"""Constants."""

########################################################################
# Cache
########################################################################
REDIS_PARAMS = {
    'host': 'redis',
    'port': 6379,
    'db': 0,
    'decode_responses': True,
}
CACHE_STORAGE_TIME = 10
"""The number of seconds the value should be stored in the cache
(`int`).
"""

########################################################################
# Attributes
########################################################################
ALIAS = 'alias'
ACTION = 'action'
GET = 'GET'
HUMANLY = 'humanly'
CATEGORY = 'category'
CATEGORIES = 'categories'
PERIOD_START_DATE = 'period_start_date'
PERIOD_END_DATE = 'period_end_date'
POST = 'POST'
PROGRESS = 'progress'
ID = 'id'
KNOW = 'know'
NOT_KNOW = 'not_know'
USER = 'user'
TERM = 'term'

########################################################################
# Variables
########################################################################
DEFAULT_PERIOD_START_INDEX = -1
DEFAULT_PERIOD_END_INDEX = 0
DEFAULT_CATEGORY = None

INCREMENT_STEP = 1  # the step value does not change
DECREMENT_STEP = -1  # the step value does not change

########################################################################
# Collections
########################################################################
DEFAULT_GLOSSARY_PARAMS = {
    PERIOD_START_DATE: DEFAULT_PERIOD_START_INDEX,
    PERIOD_END_DATE: DEFAULT_PERIOD_END_INDEX,
    CATEGORY: DEFAULT_CATEGORY,
}
"""Default choice for Glossary exercise lookup conditions
(`dict[str, int | None]`)
"""

########################################################################
# Edge date periods
########################################################################
DEFAULT_START_PERIOD = 'NC'
DEFAULT_END_PERIOD = 'DT'

EDGE_PERIOD_CHOICES = [
    ('DT', 'Сегодня'),
    ('D3', 'Три дня назад'),
    ('W1', 'Неделя назад'),
    ('W2', 'Две недели назад'),
    ('W3', 'Три недели назад'),
    ('W4', 'Четыре недели назад'),
    ('W7', 'Семь недель назад'),
    ('M3', 'Три месяца назад'),
    ('M6', 'Шесть месяцев назад'),
    ('M9', 'Девять месяцев назад'),
    ('NC', 'Добавлено'),
]
EDGE_PERIOD_ALIASES = [
    {ALIAS: 'DT', HUMANLY: 'Сегодня'},
    {ALIAS: 'D3', HUMANLY: 'Три дня назад'},
    {ALIAS: 'W1', HUMANLY: 'Неделя назад'},
    {ALIAS: 'W2', HUMANLY: 'Две недели назад'},
    {ALIAS: 'W3', HUMANLY: 'Три недели назад'},
    {ALIAS: 'W4', HUMANLY: 'Четыре недели назад'},
    {ALIAS: 'W7', HUMANLY: 'Семь недель назад'},
    {ALIAS: 'M3', HUMANLY: 'Три месяца назад'},
    {ALIAS: 'M6', HUMANLY: 'Шесть месяцев назад'},
    {ALIAS: 'M9', HUMANLY: 'Девять месяцев назад'},
    {ALIAS: 'NC', HUMANLY: 'Добавлено'},
]
"""Edge period aliases at word adding for choice
(`list[dict[str, str]]`).
"""
EDGE_PERIOD_ARGS = {
    'DT': {'days': 0},
    'D3': {'days': 3},
    'W1': {'weeks': 1},
    'W2': {'weeks': 2},
    'W3': {'weeks': 3},
    'W4': {'weeks': 4},
    'W7': {'weeks': 7},
    'M3': {'weeks': 13},
    'M6': {'weeks': 26},
    'M9': {'weeks': 40},
}
"""The datetime.timedelta args representation of period aliases at word
adding for study (`dict[str, dict[str, int]]`).

Include fields:
    ``key`` : `str`
        Period alias at word adding for study.
    ``value`` : `dict[str, int]]`
        Period of time at word adding for study.
            ``key`` : `str`
                The ``datetime.timedelta`` function argument name.
            ``value`` : `int`
                The ``datetime.timedelta`` function argument value.
"""

########################################################################
# Study progress
########################################################################
PROGRESS_MIN = 0
PROGRESS_STUDY_MAX = 6
PROGRESS_REPETITION_MAX = 7
PROGRESS_EXAMINATION_MAX = 10
PROGRESS_MAX = 11
DEFAULT_PROGRESS = 'S'

PROGRESS_CHOICES = (
    ('S', 'Изучаю'),  # study
    ('R', 'Повторяю'),  # repeat
    ('E', 'Проверяю'),  # examination
    ('K', 'Знаю'),  # know
)
PROGRESS_ALIASES = [
    {ALIAS: 'S', HUMANLY: 'Изучаю'},
    {ALIAS: 'R', HUMANLY: 'Повторяю'},
    {ALIAS: 'E', HUMANLY: 'Проверяю'},
    {ALIAS: 'K', HUMANLY: 'Знаю'},
]
"""Progres aliases (`list[dict[str, str]]`).
"""
PROGRESS_EDGES = {
    'S': [*range(PROGRESS_MIN, PROGRESS_STUDY_MAX + 1)],
    'R': [*range(PROGRESS_STUDY_MAX + 1, PROGRESS_REPETITION_MAX + 1)],
    'E': [*range(PROGRESS_REPETITION_MAX + 1, PROGRESS_EXAMINATION_MAX + 1)],
    'K': [PROGRESS_MAX],
}
"""A literal representation of an knowledge assessment
(`dict[str, list[int]]`).

Include fields:
    ``key`` : `str`
        A literal representation of an knowledge assessment.
        Where:
        'S' - is a word in the process of studied;
        'R' - word in process of repetition;
        'E' - is a word in the process of examination;
        'K' - the word has been studied.
    ``value`` : `int`
        A digital range representation of an knowledge assessment.
"""
PROGRES_STEPS = {
    KNOW: INCREMENT_STEP,
    NOT_KNOW: DECREMENT_STEP,
}

########################################################################
# Other English choices
########################################################################
LANGUAGE_ORDER = [
    ('RN', 'Перевод в случайном порядке'),
    ('EN', 'Перевод с английского языка'),
    ('RU', 'Перевод на английский язык'),
]
DEFAULT_LANGUAGE_ORDER = LANGUAGE_ORDER[0]

DEFAULT_WORD_COUNT = ('OW', 'CB')
WORD_COUNT = (
    ('OW', 'Слово'),
    ('CB', 'Словосочетание'),
    ('PS', 'Часть предложения'),
    ('ST', 'Предложение'),
)

DEFAULT_CREATE_CHOICE_VALUE = 0
DEFAULT_TIMEOUT = 5
