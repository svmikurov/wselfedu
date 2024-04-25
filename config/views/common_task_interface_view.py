from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from contrib_app.task.task import task


class CommonTaskInterfaceView(TemplateView):
    """Common task interface view."""

    def get(self, request, *args, **kwargs):
        subject_name = request.session['subject_name']
        subject_attrs = request.session['subject_attrs']
        timeout = subject_attrs.pop('timeout')

        task.set_subject(subject_name)
        task.apply_subject(**subject_attrs)

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            return JsonResponse(
                data={
                    'task': {
                        'question_text': task.question_text,
                        'answer_text': task.answer_text,
                        'timeout': timeout,
                    }
                },
                status=200,
            )
        else:
            context = {
                'timeout': timeout,
            }
            return render(request, 'common_task.html', context)
