"""
The page with exercises.

Contain available exercises.
"""

from django.views.generic import TemplateView


class IndexTaskView(TemplateView):
    """Index tasks view."""

    template_name = 'task/index.html'
