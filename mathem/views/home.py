from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home page for the subject Mathematics."""

    template_name = 'mathem/home.html'
    extra_context = {
        'title': 'Математика',
    }
