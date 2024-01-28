from english.services.serve_query import get_lookup_parameters


def save_lookup_parameters_to_session(request):
    """Сохрани в сессии параметры поиска слова для вопроса."""
    querydict = dict(request.GET.lists())
    lookup_parameters = get_lookup_parameters(querydict)
    request.session['lookup_parameters'] = lookup_parameters
