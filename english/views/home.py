from django.views.generic import TemplateView


class HomeEnglishView(TemplateView):
    """Home page for the subject English."""

    template_name = 'eng/home.html'
    extra_context = {
        'title': 'Английский язык',
    }
