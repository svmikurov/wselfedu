from english.services.serve_query import create_lookup_parameters
from english.services.serve_task_data import TaskData


def set_lookup_parameters(request) -> None:
    """Сохрани в класс TaskData параметры поиска слова для упражнения.

    Создаст параметры фильтрации для поиска.
    Сохранит параметры фильтрации в класс TaskData.
    """
    querydict = dict(request.GET.lists())
    lookup_parameters = create_lookup_parameters(querydict)
    task_data = TaskData
    task_data.lookup_parameters = lookup_parameters


def get_lookup_parameters() -> dict:
    """Получи из TaskData параметры для фильтра слов."""
    task_data = TaskData
    lookup_parameters = task_data.lookup_parameters
    return lookup_parameters
