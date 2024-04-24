from django.shortcuts import render
from django.views.generic import TemplateView

from contrib_app.task import mul_subject, task


class CommonTaskInterfaceView(TemplateView):
    """Common task interface view."""

    template_name = 'common_task_interface.html'

    def get(self, request, **kwargs):
        """Get task."""
        mul_subject.set_subject_params(min_number=2, max_number=8)
        task.set_task_subject(mul_subject)
        context = {
            'task': task,
        }
        return render(request, self.template_name, context=context)
