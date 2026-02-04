from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import re
from google.auth.transport.requests import Request
import json

# Define the required API scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/presentations.readonly'
]


def authenticate(credentials_file: str, token_file: str) -> Credentials:
    """
    Authenticate and return valid credentials for Google API.

    Parameters:
        credentials_file (str): Path to the `credentials.json` file.
        token_file (str): Path to save the `token.json` file.

    Returns:
        Credentials: Authenticated Google API credentials.
    """
    creds = None

    # Check if token.json already exists (to reuse the token)
    try:
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    except Exception:
        pass

    # If no valid token exists, initiate the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

            # Save the credentials for future use
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

    return creds


def download_original_file(shared_link: str, output_file: str, credentials_file: str, token_file: str):
    """
    Download a Google Drive file in its original format.

    Parameters:
        shared_link (str): The shareable link with edit permissions.
        output_file (str): The path to save the downloaded file.
        credentials_file (str): Path to your `credentials.json` file.
        token_file (str): Path to your `token.json` file.
    """
    # Extract the file ID from the shareable link
    match = re.search(r"/d/([^/]+)/", shared_link)
    if not match:
        raise ValueError("Invalid Google Drive shareable link format.")
    file_id = match.group(1)

    # Authenticate and get the credentials
    creds = authenticate(credentials_file, token_file)
    service = build('drive', 'v3', credentials=creds)

    # Get the file's metadata to confirm the original file type
    file_metadata = service.files().get(fileId=file_id, fields="name, mimeType").execute()
    print(f"File name: {file_metadata['name']}")
    print(f"File MIME type: {file_metadata['mimeType']}")

    # Request to download the file in its original format
    request = service.files().get_media(fileId=file_id)

    # Write the file to the output location
    with io.FileIO(output_file, "wb") as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")

    print(f"File downloaded successfully: {output_file}")

    return True


def get_file_as_json(shared_link: str, credentials_file: str, token_file: str, output_file: str = None) -> dict:
    """
    Get the JSON representation of a Google Workspace file (Docs, Sheets, Slides).

    This function uses the appropriate Google Workspace API to retrieve the structured
    JSON representation of the file, similar to what you'd get from the native APIs.

    Parameters:
        shared_link (str): The shareable Google Drive link.
        credentials_file (str): Path to your `credentials.json` file.
        token_file (str): Path to your `token.json` file.
        output_file (str, optional): Path to save the JSON output. If None, returns dict only.

    Returns:
        dict: JSON representation of the file content.

    Raises:
        ValueError: If the file type is not supported or link format is invalid.
    """
    # Extract the file ID from the shareable link
    match = re.search(r"/d/([^/]+)/", shared_link)
    if not match:
        raise ValueError("Invalid Google Drive shareable link format.")
    file_id = match.group(1)

    # Authenticate and get the credentials
    creds = authenticate(credentials_file, token_file)

    # Build Drive service to check file type
    drive_service = build('drive', 'v3', credentials=creds)
    file_metadata = drive_service.files().get(fileId=file_id, fields="name, mimeType").execute()

    mime_type = file_metadata['mimeType']
    file_name = file_metadata['name']

    print(f"File name: {file_name}")
    print(f"File MIME type: {mime_type}")

    result = None

    # Handle different Google Workspace file types
    if mime_type == 'application/vnd.google-apps.document':
        # Google Docs
        docs_service = build('docs', 'v1', credentials=creds)
        result = docs_service.documents().get(documentId=file_id).execute()
        print("Retrieved Google Doc as JSON")

    elif mime_type == 'application/vnd.google-apps.spreadsheet':
        # Google Sheets
        sheets_service = build('sheets', 'v4', credentials=creds)
        result = sheets_service.spreadsheets().get(
            spreadsheetId=file_id,
            includeGridData=True
        ).execute()
        print("Retrieved Google Sheet as JSON")

    elif mime_type == 'application/vnd.google-apps.presentation':
        # Google Slides
        slides_service = build('slides', 'v1', credentials=creds)
        result = slides_service.presentations().get(presentationId=file_id).execute()
        print("Retrieved Google Slides as JSON")

    elif mime_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                       'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                       'application/msword',
                       'application/vnd.ms-excel',
                       'application/vnd.ms-powerpoint']:
        # Microsoft Office files - these need to be converted to Google format first
        # or downloaded and parsed separately
        raise ValueError(
            f"File type '{mime_type}' is a Microsoft Office file. "
            "To get JSON representation, either:\n"
            "1. Convert to Google Workspace format in Drive, or\n"
            "2. Download the file and use a library like python-docx, openpyxl, or python-pptx"
        )

    else:
        raise ValueError(
            f"Unsupported file type: {mime_type}. "
            "This function supports Google Docs, Sheets, and Slides."
        )

    # Optionally save to file
    if output_file and result:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"JSON saved to: {output_file}")

    return result


def extract_text_from_doc_json(doc_json: dict) -> str:
    """
    Extract plain text from a Google Docs JSON representation.

    Parameters:
        doc_json (dict): The JSON object returned from the Docs API.

    Returns:
        str: Extracted plain text content.
    """
    text_content = []

    if 'body' in doc_json and 'content' in doc_json['body']:
        for element in doc_json['body']['content']:
            if 'paragraph' in element:
                for text_element in element['paragraph'].get('elements', []):
                    if 'textRun' in text_element:
                        text_content.append(text_element['textRun'].get('content', ''))

    return ''.join(text_content)


def extract_data_from_sheet_json(sheet_json: dict) -> dict:
    """
    Extract data from a Google Sheets JSON representation.

    Parameters:
        sheet_json (dict): The JSON object returned from the Sheets API.

    Returns:
        dict: Dictionary mapping sheet names to their data (list of lists).
    """
    sheets_data = {}

    for sheet in sheet_json.get('sheets', []):
        sheet_title = sheet['properties']['title']
        rows = []

        if 'data' in sheet and len(sheet['data']) > 0:
            grid_data = sheet['data'][0]

            for row_data in grid_data.get('rowData', []):
                row = []
                for cell in row_data.get('values', []):
                    # Try to get formatted value first, then effective value
                    if 'formattedValue' in cell:
                        row.append(cell['formattedValue'])
                    elif 'effectiveValue' in cell:
                        value = cell['effectiveValue']
                        # Extract the actual value based on type
                        if 'stringValue' in value:
                            row.append(value['stringValue'])
                        elif 'numberValue' in value:
                            row.append(value['numberValue'])
                        elif 'boolValue' in value:
                            row.append(value['boolValue'])
                        else:
                            row.append('')
                    else:
                        row.append('')
                rows.append(row)

        sheets_data[sheet_title] = rows

    return sheets_data


# Example usage
if __name__ == "__main__":
    # Example: Get JSON representation of a Google Doc
    shared_link = "https://docs.google.com/document/d/1NyI4xID75sY3UvjT9iQPLIJvMCh0luh0AJYsDdD2KJU/edit"
    credentials_file = "credentials.json"
    token_file = "token.json"

    try:
        # Get the JSON representation
        doc_json = get_file_as_json(
            shared_link=shared_link,
            credentials_file=credentials_file,
            token_file=token_file,
            output_file="output.json"
        )

        # Extract plain text if it's a Google Doc
        if 'body' in doc_json:
            text = extract_text_from_doc_json(doc_json)
            print("\n--- Extracted Text ---")
            print(text[:500])  # Print first 500 characters

    except Exception as e:
        print(f"Error: {e}")