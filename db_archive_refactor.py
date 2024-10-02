"""Rename the database fields of archive json file."""

import json

READE_FILE_PATH = 'db-wse-sweb-reade.json'
WRIGHT_FILE_PATH = 'db-wse-sweb.json'


def reade_json_file(file_path: str) -> list[dict]:
    """Read the json file."""
    with open(file_path, 'r') as file:
        file_data = json.load(file)
    return file_data


def wright_json_file(file_path: str, data: list[dict]) -> None:
    """Wright data to json file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def update_file_data(file_data: list[dict]) -> list[dict]:
    """Update word data."""
    for node in file_data:
        sub_node = node['fields']

        if node.get('model') == 'glossary.glossarycategory':
            sub_node['name'] = sub_node.pop('category')
            sub_node['user_id'] = 1

        if node.get('model') == 'glossary.glossary':
            sub_node['user_id'] = 1

        if node.get('model') == 'english.wordmodel':
            sub_node['foreign_word'] = sub_node.pop('word_eng')
            sub_node['russian_word'] = sub_node.pop('word_rus')
            try:
                sub_node['progress'] = sub_node.pop('knowledge_assessment')
            except KeyError:
                pass

        if node.get('model') == 'english.wordprogress':
            sub_node['progress'] = sub_node.pop('knowledge_assessment')

        if node['model'] == 'english.categorymodel':
            node['model'] = 'english.wordcategory'

    return file_data


def main() -> None:
    """Run script."""
    data = reade_json_file(READE_FILE_PATH)
    updated_data = update_file_data(data)
    wright_json_file(WRIGHT_FILE_PATH, updated_data)


if __name__ == '__main__':
    main()
