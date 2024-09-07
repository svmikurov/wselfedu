"""Constants."""

ALIAS = 'alias'
HUMANLY = 'humanly'

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

CATEGORY = 'category'
PERIOD_START_DATE = 'period_start_date'
PERIOD_END_DATE = 'period_end_date'
DEFAULT_PERIOD_START_INDEX = -1
DEFAULT_PERIOD_END_INDEX = 0
DEFAULT_CATEGORY = None

DEFAULT_GLOSSARY_PARAMS = {
    PERIOD_START_DATE: DEFAULT_PERIOD_START_INDEX,
    PERIOD_END_DATE: DEFAULT_PERIOD_END_INDEX,
    CATEGORY: DEFAULT_CATEGORY,
}
