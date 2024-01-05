"""
Модуль для автоматизации замены источники слов модели WordModel.
"""
import copy
import json
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

NEW_SOURCE_ID = 8
REPLACEABLE_SOURCES_ID = [2, 4, 5]
PATH_TO_LOADED_JSON = '../db_from_app_words.json'
PATH_TO_SAVE_JSON = '../db_with_replaces_words_sources.json'


def load_json_db_data(path_to_file):
    with open(path_to_file, 'r') as f:
        data = json.load(f)
    logging.debug('Файл json прочитан.')
    return data


def replace_source_id_words(words, new_source_id, replaceable_sources):
    new_words = copy.deepcopy(words)

    for word in new_words:
        current_word_source = word['fields']['source']
        if current_word_source in replaceable_sources:
            word['fields']['source'] = new_source_id

    if new_words != words:
        logging.debug('Произведена замена категорий.')

    return new_words


def save_json_new_db_data(path_to_file, data):
    with open(path_to_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        logging.debug(f'Файл json записан по пути "{path_to_file}".')


def replace_source_id(
        new_source_id,
        replaceable_sources,
        path_to_loaded_json,
        path_to_save_json
):
    logging.debug('Модуль запущен.')

    words_data = load_json_db_data(path_to_loaded_json)
    new_data = replace_source_id_words(
        words_data,
        new_source_id,
        replaceable_sources
    )
    save_json_new_db_data(path_to_save_json, new_data)
    logging.debug('Модуль завершил работу.')


if __name__ == '__main__':
    logging.debug('Запускаем модуль.')
    replace_source_id(
        NEW_SOURCE_ID,
        REPLACEABLE_SOURCES_ID,
        PATH_TO_LOADED_JSON,
        PATH_TO_SAVE_JSON,
    )
