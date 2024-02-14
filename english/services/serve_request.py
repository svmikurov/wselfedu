"""
Модуль для работы с request.
"""


from english.forms import WordChoiceHelperForm
from english.services.serve_query import create_lookup_params


def set_lookup_params(request) -> dict or None:
    """Установи параметры для фильтра слов.
    """
    form = WordChoiceHelperForm(request.POST)
    user_id = request.user.id

    if form.is_valid():
        form_data = form.cleaned_data
        lookup_params = create_lookup_params(form_data, user_id)

        return lookup_params


def save_lookup_params(request, lookup_params) -> None:
    """Сохрани параметры для фильтра слов.
    """
    request.session['lookup_params'] = lookup_params


def get_lookup_params(request) -> dict:
    """Получи параметры для фильтра слов.
    """
    lookup_params = request.session.get('lookup_params')
    return lookup_params
