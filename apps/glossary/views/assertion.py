"""View for assertion of a specific term."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.users.models import CustomUser

from ..models import Term, TermAssertion


class AssertionCreateView(
    LoginRequiredMixin,
    CreateView,  # type: ignore[type-arg]
):
    """Create assertion view."""

    model = TermAssertion
    fields = ['term', 'assertion']
    success_url = reverse_lazy('glossary:assertion_create')

    def get_form(self, form_class: type | None = None) -> object:
        """Filter term by user."""
        form = super().get_form(form_class)
        user = self.request.user
        if isinstance(user, CustomUser):
            form.fields['term'].queryset = Term.objects.filter(user=user)
        return form
