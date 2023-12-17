from django.views.generic import TemplateView


class HomeEnglishView(TemplateView):
    """
    Home page for the subject "English".
    Navigation on the page through theoretical material and tasks
    is transmitted using dictionaries.
    The dictionary contains the name of the item and a link to it.
    """

    # Theoretical Chapters
    chapters = {
        'Словарь': 'eng:word_list',
        'Добавить слово': 'eng:word_create',
    }

    # Solutions
    solutions = {
        'Повторить слова': 'eng:start_repetition',
        # 'Тест': '#',
    }

    extra_context = {
        'title': 'Английский язык',
        'chapters': chapters,
        'solutions': solutions,
    }
