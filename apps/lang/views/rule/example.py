"""Rule example/exception views."""

from django.views import generic


class ClauseExampleView(generic.TemplateView):
    """Rule example view."""


class RuleExceptionView(generic.TemplateView):
    """Rule example view."""
