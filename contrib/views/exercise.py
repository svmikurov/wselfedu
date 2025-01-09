"""Base exercise views."""

from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from contrib.views.general import CheckLoginPermissionMixin


class ExerciseParamsView(CheckLoginPermissionMixin, TemplateView):
    """Term term exercise conditions choice view."""

    template_name = ''
    """The exercise params view template path (`str`).
    """
    exercise_url = ''
    """URL of the exercise to redirect to after selecting parameters
    (`str`).
    For example::

       exercise_url = reverse_lazy('glossary:exercise')
    """
    form = None
    """The exercise params form (`Form`).
    """

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add exercise params form to context."""
        context = super().get_context_data()
        context['form'] = self.form(request=self.request)
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        """Get user task condition."""
        form = self.form(request.POST, request=request)
        user = request.user

        if form.is_valid():
            task_conditions = form.clean()

            if task_conditions.pop('save_params'):
                self.save_params(user, task_conditions)

            task_conditions['user_id'] = user.id
            request.session['task_conditions'] = task_conditions
            return redirect(self.exercise_url)

        context = {'form': self.form(request=self.request)}
        return render(request, self.template_name, context)

    def save_params(
        self,
        user: AbstractBaseUser,
        task_conditions: dict,
    ) -> None:
        """Save the user exercise params to database.

        :param AbstractBaseUser user: The current user.
        :param dict task_conditions: The task conditions to save.
        :raises NotImplementedError: if the method is not overridden.
        """
        raise NotImplementedError('The method save_params is not implemented')
