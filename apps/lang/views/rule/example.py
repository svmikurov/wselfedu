"""Rule clause edit example/exception views."""

from apps.core.views.edit import BaseAddView
from apps.lang import forms


class TaskExampleAddView(BaseAddView):
    """Add rule clause task example view."""

    form_class = forms.TaskExampleForm


class WordExampleAddView(BaseAddView):
    """Add rule clause word example view."""

    form_class = forms.WordExampleForm


class ExceptionAddView(BaseAddView):
    """Add rule clause word example view."""

    # TODO: Implement a view to add an exception to a rule clause
    # Add `form_class`
