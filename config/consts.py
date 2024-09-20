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

TERM_PROGRES_MIN = 0
TERM_PROGRES_MAX = 11
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

PROGRES_STEPS = {
    KNOW: INCREMENT_STEP,
    NOT_KNOW: DECREMENT_STEP,
}

########################################################################
# Collections for Model choices
########################################################################

EDGE_PERIOD_ITEMS = [
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
"""Edge periods, for choice (`dict[str, str]`).
"""
PROGRES_STAGES = [
    {ALIAS: 'S', HUMANLY: 'Изучаю'},
    {ALIAS: 'R', HUMANLY: 'Повторяю'},
    {ALIAS: 'E', HUMANLY: 'Проверяю'},
    {ALIAS: 'K', HUMANLY: 'Знаю'},
]
"""Study progres stages, for choice (`dict[str, str]`).
"""
