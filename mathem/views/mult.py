from django.views.generic import TemplateView


class MultTaskView(TemplateView):
    extra_context = {
        'title': 'Таблица умножения'
    }
