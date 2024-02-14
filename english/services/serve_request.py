from english.services.serve_query import create_lookup_parameters


def save_lookup_parameters(request, lookup_parameters) -> None:
    """Сохрани параметры поиска слова для упражнения."""
    request.session['lookup_params'] = lookup_parameters


def set_lookup_parameters(request) -> None:
    """Установи параметры поиска слова для упражнения.

    Создаст параметры фильтрации для поиска.
    Сохранит параметры фильтрации.
    """
    querydict = dict(request.GET.lists())
    lookup_parameters = create_lookup_parameters(querydict)
    save_lookup_parameters(request, lookup_parameters)


def get_lookup_parameters(request) -> dict:
    """Получи параметры для фильтра слов."""
    lookup_params = request.session.get('lookup_params')
    return lookup_params
