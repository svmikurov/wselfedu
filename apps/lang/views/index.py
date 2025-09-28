"""Language discipline index view."""

from django.views.generic import TemplateView


class IndexLangView(TemplateView):
    """Language discipline index view."""

    template_name = 'lang/index.html'
