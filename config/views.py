from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home view."""

    template_name = 'home.html'
    extra_context = {
        'title': 'WSE: Домашняя страница',
    }


class MathHomeView(TemplateView):
    """Math home view."""

    template_name = 'mathem/home.html'
    extra_context = {
        'title': 'Математика',
    }
