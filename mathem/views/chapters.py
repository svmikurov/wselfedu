from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    A page with chapters on mathematics.
    Contains links to these chapters.
    """
    chapters = {
        'Таблица умножения': 'math:mult',
    }
    extra_context = {
        'title': 'Математика',
        'chapters': chapters,
    }
