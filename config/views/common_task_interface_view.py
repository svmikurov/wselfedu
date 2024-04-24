from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from contrib_app.task.task import task


class CommonTaskInterfaceView(TemplateView):
    """Common task interface view."""

    template_name = 'common_task.html'

    def get(self, request, *args, **kwargs):
        subject_name = request.session['subject_name']
        subject_attrs = request.session['subject_attrs']

        task.set_subject(subject_name)
        task.apply_subject(**subject_attrs)

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            return JsonResponse(
                data={
                    'task': {
                        'question_text': task.question_text,
                        'answer_text': task.answer_text,
                    }
                },
                status=200,
            )
        else:
            context = {
                'task': task,
            }
            return render(request, self.template_name, context)
