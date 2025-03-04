from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import re
from google.auth.transport.requests import Request

# Define the required API scope
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

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
        # if creds and creds.expired and creds.refresh_token:
        #     # print('Credentials expired')
        #     creds.refresh(Request())
    # else:
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