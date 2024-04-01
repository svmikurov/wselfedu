from django.views.generic import TemplateView

TITLE = {
    'add': 'Сложение',
    'sub': 'Вычитание',
    'mult': 'Умножение',
}


class CalculationsView(TemplateView):
    template_name = 'mathem/calculations.html'
    extra_context = {
        'title': 'Вычисления',
    }
