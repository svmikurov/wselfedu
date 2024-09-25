"""Constants."""

GET = 'GET'
POST = 'POST'

########################################################################
# Attributes
########################################################################

ALIAS = 'alias'
ACTION = 'action'
HUMANLY = 'humanly'
CATEGORY = 'category'
CATEGORIES = 'categories'
PERIOD_START_DATE = 'period_start_date'
PERIOD_END_DATE = 'period_end_date'
PROGRES = 'progres'
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

WORD_PROGRES_MIN = 0
WORD_PROGRES_MAX = 11


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

PROGRES_STEPS = {
    KNOW: INCREMENT_STEP,
    NOT_KNOW: DECREMENT_STEP,
}

########################################################################
# Model choices
########################################################################
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
('alias', 'representation'), (`list[tuple[str, str]]`).
"""
DEFAULT_START_PERIOD = 'NC'
DEFAULT_END_PERIOD = 'DT'

########################################################################
# Study progres.
########################################################################
PROGRES_CHOICES = (
    ('S', 'Изучаю'),  # study
    ('R', 'Повторяю'),  # repeat
    ('E', 'Проверяю'),  # examination
    ('K', 'Знаю'),  # know
)
PROGRES_STAGE_ALIASES = [
    {ALIAS: 'S', HUMANLY: 'Изучаю'},
    {ALIAS: 'R', HUMANLY: 'Повторяю'},
    {ALIAS: 'E', HUMANLY: 'Проверяю'},
    {ALIAS: 'K', HUMANLY: 'Знаю'},
]
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
DEFAULT_PROGRES = 'S'
PROGRES_MIN = 0
PROGRES_STUDY_MAX = 6
PROGRES_REPETITION_MAX = 7
PROGRES_EXAMINATION_MAX = 10
PROGRES_MAX = 11
PROGRES_STAGE_EDGES = {
    'S': [*range(PROGRES_MIN, PROGRES_STUDY_MAX + 1)],
    'R': [*range(PROGRES_STUDY_MAX + 1, PROGRES_REPETITION_MAX + 1)],
    'E': [*range(PROGRES_REPETITION_MAX + 1, PROGRES_EXAMINATION_MAX + 1)],
    'K': [PROGRES_MAX],
}

########################################################################
# English application
########################################################################

LANGUAGE_ORDER = [
    ('RN', 'Перевод в случайном порядке'),
    ('EN', 'Перевод с английского языка'),
    ('RU', 'Перевод на английский язык'),
]
DEFAULT_LANGUAGE_ORDER = LANGUAGE_ORDER[0]
WORD_COUNT = (
    ('OW', 'Слово'),
    ('CB', 'Словосочетание'),
    ('PS', 'Часть предложения'),
    ('ST', 'Предложение'),
)
DEFAULT_WORD_COUNT = ('OW', 'CB')
DEFAULT_CREATE_CHOICE_VALUE = 0
DEFAULT_TIMEOUT = 5

# DEFAULT_START_PERIOD_INDEX = -1
# DEFAULT_END_PERIOD_ALIAS = 0
# DEFAULT_PROGRES_INDEX = 0
# ALIAS_INDEX = 0
