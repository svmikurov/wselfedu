"""Rename the database fields of archive json file."""

import json

READE_FILE_PATH = 'db-wse-sweb-2024-11-11.json'
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


def rename_node_fields(data: list[dict]) -> list[dict]:  # noqa: C901
    """Rename node fields."""

    for node in data:

        if node.get('model') == "foreign.translateparams":
            fields: dict = node['fields']
            fields['progress'] = str([fields['progress']]).replace("'", '"')

        if node.get('model') == "glossary.glossaryparams":
            fields: dict = node['fields']
            fields['progress'] = str([fields['progress']]).replace("'", '"')

    return data


def main() -> None:
    """Run script."""
    data = reade_json_file(READE_FILE_PATH)
    updated_data = rename_node_fields(data)
    wright_json_file(WRIGHT_FILE_PATH, updated_data)


if __name__ == '__main__':
    main()
