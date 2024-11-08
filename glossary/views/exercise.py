"""Views for term study."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from contrib.views import (
    CheckLoginPermissionMixin,
)
from glossary.forms.term_choice import GlossaryParamsForm
from glossary.models import GlossaryCategory, GlossaryParams, TermSource


class GlossaryParamsView(CheckLoginPermissionMixin, TemplateView):
    """Glossary term exercise conditions choice view."""

    template_name = 'glossary/exercise/params.html'
    """The view template path (`str`).
    """

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add exercise params form to context."""
        context = super().get_context_data()
        context['form'] = GlossaryParamsForm(request=self.request)
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        """Get user task condition."""
        form = GlossaryParamsForm(request.POST, request=request)
        user = request.user

        if form.is_valid():
            task_conditions = form.clean()
            task_conditions['user_id'] = user.id
            to_story = task_conditions.pop('save_params')

            if to_story:
                params, _ = GlossaryParams.objects.get_or_create(user=user)
                params.favorites = task_conditions['favorites']
                params.period_start_date = task_conditions['period_start_date']
                params.period_end_date = task_conditions['period_end_date']
                params.progress = task_conditions['progress']
                params.timeout = task_conditions['timeout']

                category_id = int(task_conditions['category'])
                if category_id:
                    params.category = GlossaryCategory.objects.get(
                        pk=category_id
                    )
                else:
                    params.category = None

                source_id = int(task_conditions['source'])
                if source_id:
                    params.source = TermSource.objects.get(pk=source_id)
                else:
                    params.source = None

                params.save()

            request.session['task_conditions'] = task_conditions
            return redirect(reverse_lazy('glossary:exercise'))

        context = {'form': GlossaryParamsForm(request=self.request)}
        return render(request, self.template_name, context)
