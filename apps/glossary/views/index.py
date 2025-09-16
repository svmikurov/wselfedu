"""Index view of Glossary app."""

from django.views.generic import TemplateView


class IndexGlossaryView(TemplateView):
    """Index view of Glossary app."""

    template_name = 'glossary/index.html'
