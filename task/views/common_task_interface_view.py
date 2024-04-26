from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from task.task import task


class CommonTaskInterfaceView(TemplateView):
    """Common task interface view."""

    def get(self, request, *args, **kwargs):
        task_data = request.session['task_data']
        task.apply_subject(**task_data)

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            return JsonResponse(
                data={
                    'task': {
                        'question_text': task.question_text,
                        'answer_text': task.answer_text,
                        'timeout': task_data['timeout'],
                    }
                },
                status=200,
            )
        else:
            return render(request, 'task/common_task.html')
