"""Constants."""

########################################################################
# Variable values
########################################################################

PAGINATE_NUMBER = 20
INCREMENT_STEP = 1  # the step value does not change
DECREMENT_STEP = -1  # the step value does not change
DEFAULT_ZERO_VALUE = 0
DEFAULT_TIMEOUT = 5

########################################################################
# Messages
########################################################################

MSG_NO_TASK = 'По заданным условиям задание не сформировано'

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
HUMANLY = 'humanly'
NOT_CHOICES = 'NC'

########################################################################
# Layout constants
########################################################################

BTN_BACK = 'btn-back'
BTN_NAME = 'btn_name'
BTN_SM = 'btn-sm'
BUTTON = 'button'
COL_6 = 'col-6'
SUBMIT = 'submit'
TITLE = 'title'
VISIBLE = 'visible'
W_25 = 'w-25'
W_50 = 'w-50'
LINK = 'link'

########################################################################
# Edge date periods
########################################################################

TODAY = 'DT'
DAYS_AGO_3 = 'D3'
WEEK_AGO = 'W1'
WEEKS_AGO_2 = 'W2'
WEEKS_AGO_3 = 'W3'
WEEKS_AGO_4 = 'W4'
WEEKS_AGO_7 = 'W7'
MONTHS_AGO_3 = 'M3'
MONTHS_AGO_6 = 'M6'
MONTHS_AGO_9 = 'M9'

EDGE_PERIOD_CHOICES = [
    (TODAY, 'Сегодня'),
    (DAYS_AGO_3, 'Три дня назад'),
    (WEEK_AGO, 'Неделя назад'),
    (WEEKS_AGO_2, 'Две недели назад'),
    (WEEKS_AGO_3, 'Три недели назад'),
    (WEEKS_AGO_4, 'Четыре недели назад'),
    (WEEKS_AGO_7, 'Семь недель назад'),
    (MONTHS_AGO_3, 'Три месяца назад'),
    (MONTHS_AGO_6, 'Шесть месяцев назад'),
    (MONTHS_AGO_9, 'Девять месяцев назад'),
    (NOT_CHOICES, 'Добавлено'),
]
"""Edge period choices.
"""
EDGE_PERIOD_ALIASES = [
    {ALIAS: TODAY, HUMANLY: 'Сегодня'},
    {ALIAS: DAYS_AGO_3, HUMANLY: 'Три дня назад'},
    {ALIAS: WEEK_AGO, HUMANLY: 'Неделя назад'},
    {ALIAS: WEEKS_AGO_2, HUMANLY: 'Две недели назад'},
    {ALIAS: WEEKS_AGO_3, HUMANLY: 'Три недели назад'},
    {ALIAS: WEEKS_AGO_4, HUMANLY: 'Четыре недели назад'},
    {ALIAS: WEEKS_AGO_7, HUMANLY: 'Семь недель назад'},
    {ALIAS: MONTHS_AGO_3, HUMANLY: 'Три месяца назад'},
    {ALIAS: MONTHS_AGO_6, HUMANLY: 'Шесть месяцев назад'},
    {ALIAS: MONTHS_AGO_9, HUMANLY: 'Девять месяцев назад'},
    {ALIAS: NOT_CHOICES, HUMANLY: 'Добавлено'},
]
"""Edge period aliases at word adding for choice
(`list[dict[str, str]]`).
**DEPRECATED** - Use ``EDGE_PERIOD_CHOICES``.
"""
EDGE_PERIOD_ARGS = {
    TODAY: {'days': 0},
    DAYS_AGO_3: {'days': 3},
    WEEK_AGO: {'weeks': 1},
    WEEKS_AGO_2: {'weeks': 2},
    WEEKS_AGO_3: {'weeks': 3},
    WEEKS_AGO_4: {'weeks': 4},
    WEEKS_AGO_7: {'weeks': 7},
    MONTHS_AGO_3: {'weeks': 13},
    MONTHS_AGO_6: {'weeks': 26},
    MONTHS_AGO_9: {'weeks': 40},
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
PROGRESS_REPEAT_MAX = 8
PROGRESS_EXAMIN_MAX = 10
PROGRESS_MAX = 11

STUDY = 'S'
REPEAT = 'R'
EXAMINATION = 'E'
LEARNED = 'K'

PROGRESS_CHOICES = [
    (STUDY, 'Изучаю'),  # study
    (REPEAT, 'Повторяю'),  # repeat
    (EXAMINATION, 'Проверяю'),  # examination
    (LEARNED, 'Знаю'),  # know
]
"""Progress study items choices (`tuple[tuple[str, str]]`).
"""
DEFAULT_PROGRESS = [STUDY]
"""Default progress choice (`str`).
"""

PROGRESS_ALIASES = [
    {ALIAS: STUDY, HUMANLY: 'Изучаю'},
    {ALIAS: REPEAT, HUMANLY: 'Повторяю'},
    {ALIAS: EXAMINATION, HUMANLY: 'Проверяю'},
    {ALIAS: LEARNED, HUMANLY: 'Знаю'},
]
"""Progres aliases (`list[dict[str, str]]`).
**DEPRECATED** - Use ``PROGRESS_CHOICES``.
"""
PROGRESS_STAGE_EDGES = {
    STUDY: [*range(PROGRESS_MIN, PROGRESS_STUDY_MAX + 1)],
    REPEAT: [*range(PROGRESS_STUDY_MAX + 1, PROGRESS_REPEAT_MAX + 1)],
    EXAMINATION: [*range(PROGRESS_REPEAT_MAX + 1, PROGRESS_EXAMIN_MAX + 1)],
    LEARNED: [PROGRESS_MAX],
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
    'know': INCREMENT_STEP,
    'not_know': DECREMENT_STEP,
}

########################################################################
# The order of translation of words in the exercise
########################################################################

RANDOM = 'RN'
TO_NATIVE = 'TN'
FROM_NATIVE = 'FN'

DEFAULT_LANGUAGE_ORDER = TO_NATIVE

LANGUAGE_ORDER_CHOICE = [
    (RANDOM, 'Случайный порядок'),
    (TO_NATIVE, 'На родной'),
    (FROM_NATIVE, 'С родного'),
]
"""The order in which language translations of words are displayed
(list[tuple[str, str]]`).
"""
LANGUAGE_ORDER_ALIAS = [
    {ALIAS: RANDOM, HUMANLY: 'Случайный порядок'},
    {ALIAS: TO_NATIVE, HUMANLY: 'На родной'},
    {ALIAS: FROM_NATIVE, HUMANLY: 'С родного'},
]
"""**DEPRECATED** - Use ``LANGUAGE_ORDER_CHOICE``.
"""

########################################################################
# Collections
########################################################################

DEFAULT_CATEGORY = None
DEFAULT_SOURCE = None
DEFAULT_LOOKUP_CONDITIONS = {
    'period_start_date': NOT_CHOICES,
    'period_end_date': TODAY,
    'progress': DEFAULT_PROGRESS,
    'category': DEFAULT_CATEGORY,
    'source': DEFAULT_SOURCE,
    'count_first': 0,
    'count_last': 0,
}
"""Default choice for Term exercise lookup conditions
(`dict[str, int | None]`)
"""

########################################################################
# Reversed paths
########################################################################

CREATE_CATEGORY_PATH = 'foreign:categories_create'
CREATE_WORD_PATH = 'foreign:words_create'

DELETE_CATEGORY_PATH = 'foreign:categories_delete'
DETAIL_CATEGORY_PATH = 'foreign:categories_detail'
UPDATE_CATEGORY_PATH = 'foreign:categories_update'

CREATE_SOURCE_PATH = 'foreign:source_create'
DELETE_SOURCE_PATH = 'foreign:source_delete'
DETAIL_SOURCE_PATH = 'foreign:source_detail'
UPDATE_SOURCE_PATH = 'foreign:source_update'

DELETE_WORD_PATH = 'foreign:words_delete'
DETAIL_WORD_PATH = 'foreign:words_detail'
UPDATE_WORD_PATH = 'foreign:words_update'
WORD_LIST_PATH = 'foreign:word_list'

CATEGORY_LIST_PATH = 'foreign:category_list'
SOURCE_LIST_PATH = 'foreign:source_list'

########################################################################
# Templates
########################################################################

FORM_TEMPLATE = 'form.html'
DELETE_TEMPLATE = 'delete.html'

DETAIL_CATEGORY_TEMPLATE = 'foreign/category_detail.html'
DETAIL_SOURCE_TEMPLATE = 'foreign/source_detail.html'
DETAIL_WORD_TEMPLATE = 'foreign/word_detail.html'

CATEGORY_LIST_TEMPLATE = 'foreign/category_list.html'
SOURCE_LIST_TEMPLATE = 'foreign/source_list.html'
WORD_LIST_TEMPLATE = 'foreign/word_list.html'

########################################################################
# Mathematical operation
########################################################################

ADDITION = 'add'
SUBSTRUCTION = 'sub'
MULTIPLICATION = 'mul'
DIVISION = 'div'

CALCULATION_TYPES = (
    (ADDITION, 'Сложение'),
    (SUBSTRUCTION, 'Вычитание'),
    (MULTIPLICATION, 'Умножение'),
    # (DIVISION, 'Деление'),  # Temporary not used
)
"""Mathematical exercise type choice.

Use in choices, note: max_length=10.
"""

########################################################################
# Other constants
########################################################################

NO_SELECTION = {
    ALIAS: None,
    HUMANLY: 'Не выбрано',
}
