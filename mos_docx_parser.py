import os
import backoff
import git
from bs4 import BeautifulSoup
import json

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
        if character_data['character'].lower() == 'name':
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


if __name__ == "__main__":

    # the mammoth lib is used to convert docx to html, which is then parsed using beautiful soup
    import mammoth
    import git

    with open("mos_parser_datastore/Manual of Style.docx", "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        mos_html = result.value  # The generated HTML
        messages = result.messages  # Any messages, such as warnings during conversion

    character_notes_html = mos_html.split(split_point)[1]
    parsed_json = parse_character_html(character_notes_html)
    with open('public/mos_character_notes.json', 'w', encoding='utf-8') as json_file:
        json_file.write(parsed_json)

    working_dir = os.getcwd()
    Git.git_pull(working_dir, 'main')
    Git.git_commit_all(working_dir, 'mos character notes update')
    Git.git_push(working_dir, 'main')

