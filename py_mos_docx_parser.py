import os
import backoff
import git
from bs4 import BeautifulSoup
import json

from html.parser import HTMLParser
from io import StringIO

# List of tuples (name, replacement, suffix)
name_replacements = [
    ('Al', 'Aldebaran', 'aka Al'),
    ('Wilhelm van Astrea (née Trias)', 'Wilhelm van Astrea', '(née Trias)'),
    ('Carol Fauzen (née Remendis)', 'Carol Fauzen', '(née Remendis)')
]

# Substring that is used to split the mos at the point after which the character notes begin
split_point = 'Character Index</h1>'

class Git:

    @staticmethod
    @backoff.on_exception(
        backoff.expo,
        exception=git.GitCommandError,
        max_tries=3,
        max_time=30
    )
    def git_commit_all(repository_path, commit_message):
        try:
            repo = git.Repo(repository_path)
            repo.git.add(all=True)
            repo.index.commit(commit_message)
            print("Committed all changes successfully.")
        except git.GitCommandError as e:
            print("Error:", e)

    @staticmethod
    @backoff.on_exception(
        backoff.expo,
        exception=git.GitCommandError,
        max_tries=3,
        max_time=30
    )
    def git_push(repository_path, branch_name):
        try:
            repo = git.Repo(repository_path)
            origin = repo.remotes.origin
            origin.push(refspec=branch_name)
            print("Pushed changes successfully.")
        except git.GitCommandError as e:
            print("Error:", e)

    @staticmethod
    @backoff.on_exception(
        backoff.expo,
        exception=git.GitCommandError,
        max_tries=3,
        max_time=30
    )
    def git_pull(repository_path, branch_name):
        try:
            repo = git.Repo(repository_path)
            origin = repo.remotes.origin
            origin.pull(refspec=branch_name)
            print("Pulled changes successfully.")
        except git.GitCommandError as e:
            print("Error:", e)

def parse_character_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    characters = []

    # Find all character blocks by identifying <h4> tags
    character_blocks = soup.find_all('h4')

    for block in character_blocks:
        character_data = {}

        character_data['wip'] = True if '(WIP)' in block.get_text(strip=True) else False

        # Character name
        character_data['character'] = block.get_text(strip=True).replace('(WIP)', '').strip()
        # If name is 'Name' skip to next iteration (this is used to id template blocks)
        if character_data['character'].lower() == 'name' or not character_data['character'].lower().strip():
            continue

        character_data['name_suffix'] = ''
        for (name, replacement, suffix) in name_replacements:
            if character_data['character'] == name:
                character_data['character'] = replacement
                character_data['name_suffix'] = suffix


        # Get the subsequent sibling elements of the current block
        sibling = block.find_next_sibling()

        # Initialize fields
        character_data['name_in_jp'] = ""
        character_data['japanese_speech_quirks'] = []
        character_data['english_speech_quirks'] = []
        character_data['notes'] = []


        while sibling:
            # Extract "Name in Japanese"
            if sibling.name == 'p' and 'Name in Japanese:' in sibling.get_text():
                character_data['name_in_jp'] = sibling.get_text(strip=True).split(': ')[1] if len(sibling.get_text(strip=True).split(': ')) > 1 else ''

            # Extract "Japanese speech quirks"
            elif sibling.name == 'ul' and sibling.find_previous_sibling('p') and 'Japanese speech quirks:' in sibling.find_previous_sibling('p').get_text():
                for li in sibling.find_all('li'):
                    character_data['japanese_speech_quirks'].append(li.get_text(strip=True))

            # Extract "English speech quirks"
            elif sibling.name == 'ul' and sibling.find_previous_sibling('p') and 'English speech quirks:' in sibling.find_previous_sibling('p').get_text():
                for li in sibling.find_all('li'):
                    character_data['english_speech_quirks'].append(li.get_text(strip=True))

            # Extract "Notes"
            elif sibling.name == 'ul' and sibling.find_previous_sibling('p') and 'Notes:' in sibling.find_previous_sibling('p').get_text():
                for li in sibling.find_all('li'):
                    character_data['notes'].append(li.get_text(strip=True))

            # Stop at the next <h4> tag (next character)
            if sibling.name == 'h4':
                break

            sibling = sibling.find_next_sibling()

        characters.append(character_data)

    return json.dumps(characters, indent=2, ensure_ascii=False)


import csv
import io
from typing import List, Dict, Union


def csv_to_json(data: Union[str, io.IOBase], is_file: bool = False) -> Union[List[Dict[str, str]], str]:
    """
    Convert CSV data to a list of dictionaries.

    Args:
        data: Either a CSV string or a file object
        is_file: True if data is a file object, False if it's a CSV string

    Returns:
        List of dictionaries where keys are column headers, or error message string
    """
    try:
        # Handle file object vs string input
        if is_file:
            csv_reader = csv.DictReader(data)
        else:
            # Print first 200 chars for debugging
            # print(f"DEBUG - First 200 chars of input: {repr(data[:200])}")
            csv_reader = csv.DictReader(io.StringIO(data))

        # Debug: print the fieldnames
        # print(f"DEBUG - Field names detected: {csv_reader.fieldnames}")
        # print(f"DEBUG - Number of fields: {len(csv_reader.fieldnames) if csv_reader.fieldnames else 0}")

        def process_cell_value(string):
            if (string.startswith('[') and string.endswith(']')) or (string.startswith('{') and string.endswith('}')):
                try:
                    json_value = json.loads(string)
                    return json_value
                except Exception as e:
                    print(e)

            return string


        result = []

        # Process each row
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                row_dict = {key: (process_cell_value(value) if value is not None else '') for key, value in row.items()}
                result.append(row_dict)
            except Exception as e:
                return f"Error processing row {row_num}: {str(e)}"

        return result

    except Exception as e:
        return f"Error reading CSV data: {str(e)}"


def html_table_to_csv(html_string):
    """
    Convert an HTML table to CSV format using BeautifulSoup.
    Cells with multiple paragraphs will be represented as JSON lists.

    Args:
        html_string (str): HTML string containing a table

    Returns:
        str: CSV formatted string
    """

    # Parse the HTML
    soup = BeautifulSoup(html_string, 'html.parser')

    # Find the table
    table = soup.find('table')
    if not table:
        return ""

    rows = []

    # Process all rows
    for tr in table.find_all('tr'):
        row = []
        # Get all cells (both th and td)
        cells = tr.find_all(['th', 'td'])
        for cell in cells:
            # Find all paragraphs in the cell
            paragraphs = cell.find_all('p')

            if len(paragraphs) > 1:
                # Multiple paragraphs: create a list
                cell_value = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                # Convert list to JSON string for CSV compatibility
                row.append(json.dumps(cell_value, ensure_ascii=False))
            elif len(paragraphs) == 1:
                # Single paragraph: just get the text
                row.append(paragraphs[0].get_text(strip=True))
            else:
                # No paragraphs: get all text
                cell_text = cell.get_text(separator=' ', strip=True)
                row.append(cell_text)

        if row:  # Only add non-empty rows
            rows.append(row)

    # Convert to CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)

    return output.getvalue()


if __name__ == "__main__":
    from py_download_mos import download_original_file, download_sheet_as_csv

    # the mammoth lib is used to convert docx to html, which is then parsed using beautiful soup
    import mammoth
    import git

    # MOS Doc

    shared_link = "https://drive.google.com/file/d/12Z5Jb61kz2QGQibnIukgEjK4oIgMYX45/edit"
    output_file = "mos_parser_datastore/mos.docx"
    service_account_file = "rekai-408314-f1c11bd002a0.json"

    # Downloads the original mos docx file via the Google Drive API
    mos_dl_successful = download_original_file(shared_link, output_file, service_account_file)

    if mos_dl_successful:
        with open("mos_parser_datastore/mos.docx", "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            mos_html = result.value  # The generated HTML
            messages = result.messages  # Any messages, such as warnings during conversion

        with open('mos_parser_datastore/mos.html', 'w', encoding='utf-8') as docx_html:
            docx_html.write(mos_html)

        character_notes_html = mos_html.split(split_point)[1]
        parsed_json = parse_character_html(character_notes_html)
        with open('public/mos_character_notes.json', 'w', encoding='utf-8') as json_file:
            json_file.write(parsed_json)


    # Speaking Styles XLSX

    ss_sheet_link = "https://docs.google.com/spreadsheets/d/1NyI4xID75sY3UvjT9iQPLIJvMCh0luh0AJYsDdD2KJU/edit"
    csv_output_file = "mos_parser_datastore/speaking_styles.csv"

    speaking_styles_successful = download_sheet_as_csv(ss_sheet_link, csv_output_file, service_account_file)
    if speaking_styles_successful:
        with open(csv_output_file, 'r', encoding='utf-8') as f:
            speaking_styles_json = csv_to_json(f, is_file=True)
        with open('public/speaking_styles.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(speaking_styles_json, indent=2, ensure_ascii=False))

    with open('mos_parser_datastore/mos.html', 'r', encoding='utf-8') as mos_html_file:
        mos_html_string = mos_html_file.read()

    soup = BeautifulSoup(mos_html_string, 'html.parser')
    tables = soup.find_all('table')

    parsed_tables = []

    for table in tables:
        json_list = csv_to_json(html_table_to_csv(str(table)))
        parsed_tables.append(json_list)

    with open('public/mos_dictionary_tables.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(parsed_tables, indent=2, ensure_ascii=False))


