"""
Модуль для работы с request.
"""


def save_lookup_params(request, lookup_params) -> None:
    """Сохрани параметры для фильтра слов.
    """
    request.session['lookup_params'] = lookup_params


def get_lookup_params(request) -> dict:
    """Получи параметры для фильтра слов.
    """
    lookup_params = request.session.get('lookup_params')
    return lookup_params
