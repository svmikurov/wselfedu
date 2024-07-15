"""
Change field name WordModel words_eng, words_rus to word_eng, word_rus
"""

import json

FILE_TO_BE_FORMATTED = 'db-wse-beget-2024-05-19-wordmodel.json'
OLD_FAIL_FORMAT_PATH = f'../{FILE_TO_BE_FORMATTED}'
NEW_FAIL_NAME = 'load_words.json'


def open_file(file_path: str) -> dict:
    """Reade data from *.json"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def save_file(file_path: str, data: list[dict]):
    """Save new data to *.json"""
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def reformat_file_data(dict_path: str):
    """
    Replaces the model name in the uploaded file from the database.
    Save updated data to new *.json.
    """
    loaded_data: dict = open_file(dict_path)
    new_data: list[dict] = []

    # Replaces the model name in uploaded file
    for loaded_node in loaded_data:
        new_node = {
            'model': loaded_node['model'],
            'pk': loaded_node['pk'],
            'fields': {
                'user': loaded_node['fields']['user'],
                'word_eng': loaded_node['fields']['words_eng'],
                'word_rus': loaded_node['fields']['words_rus'],
                'source': loaded_node['fields']['source'],
                'category': loaded_node['fields']['category'],
                'word_count': loaded_node['fields']['word_count'],
                'created_at': loaded_node['fields']['created_at'],
                'updated_at': loaded_node['fields']['updated_at'],
            },
        }
        new_data.append(new_node)

    # Save new data to a file
    save_path = f'../{NEW_FAIL_NAME}'
    save_file(save_path, new_data)


if __name__ == '__main__':
    reformat_file_data(OLD_FAIL_FORMAT_PATH)
