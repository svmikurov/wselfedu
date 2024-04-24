from django.http import JsonResponse
from django.views.generic import TemplateView

from contrib_app.task.calculations import calculation_subject
from contrib_app.task.task import task


class CommonTaskInterfaceView(TemplateView):
    """Common task interface view."""

    template_name = 'common_task_interface.html'
    subject = calculation_subject
    subject_params = {'min_number': 2, 'max_number': 9, 'ops': '*'}

    def get_context_data(self, **kwargs):
        self.subject.set_subject_params(**self.subject_params)
        task.set_task_subject(self.subject)
        context = super().get_context_data()
        context['task'] = task
        return context

    def post(self, request):
        """Ajax representation task."""
        self.subject.set_subject_params(**self.subject_params)
        task.set_task_subject(self.subject)
        return JsonResponse(
            data={
                'task': {
                    'question_text': task.question_text,
                    'answer_text': task.answer_text,
                }
            },
            status=200,
        )
