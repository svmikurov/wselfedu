"""Rename the database fields of archive json file."""

import json

READE_FILE_PATH = 'db-wse-sweb-2024-10-20.json'
WRIGHT_FILE_PATH = 'db-wse-sweb.json'
DEFAULT_USER_ID = 1


def reade_json_file(file_path: str) -> list[dict]:
    """Read the json file."""
    with open(file_path, 'r') as file:
        file_data = json.load(file)
    return file_data


def wright_json_file(file_path: str, data: list[dict]) -> None:
    """Wright data to json file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def rename_node_fields(data: list[dict]) -> list[dict]:
    """Rename node fields."""
    renamed_nodes = {
        'users.usermodel': 'users.userapp',
        'english.categorymodel': 'foreign.wordcategory',
        'english.sourcemodel': 'foreign.wordsource',
        'english.wordmodel': 'foreign.word',
        'english.worduserknowledgerelation': 'foreign.wordprogress',
        'english.wordsfavoritesmodel': 'foreign.wordfavorites',
        'english.wordlearningstories': 'foreign.wordanalytics',
        'task.mathematicalexercise': 'mathematics.mathematicsanalytic',
        'task.points': 'users.points',
    }
    unnecessary_nodes = [
        'admin.logentry',
        'sessions.session',
    ]
    updated_list = []

    for node in data:
        fields: dict = node['fields']

        if node['model'] not in unnecessary_nodes:
            updated_list.append(node)

        if node['model'] in renamed_nodes:
            node['model'] = renamed_nodes[node['model']]

        if node['model'] == 'foreign.wordprogress':
            fields['progress'] = fields.pop('knowledge_assessment')

        if node['model'] == 'glossary.glossarycategory':
            fields['name'] = fields.pop('category')
            fields['user_id'] = DEFAULT_USER_ID

        elif node['model'] == 'glossary.glossary':
            fields['user_id'] = DEFAULT_USER_ID

        elif node['model'] == 'foreign.word':
            fields['foreign_word'] = fields.pop('word_eng')
            fields['native_word'] = fields.pop('word_rus')

    return updated_list


def main() -> None:
    """Run script."""
    data = reade_json_file(READE_FILE_PATH)
    updated_data = rename_node_fields(data)
    wright_json_file(WRIGHT_FILE_PATH, updated_data)


if __name__ == '__main__':
    main()
