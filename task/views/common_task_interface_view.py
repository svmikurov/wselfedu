from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from task.forms.user_input_form import NumberInputForm
from task.task import task


class CommonTaskInterfaceView(TemplateView):
    """Common task interface view."""

    def get(self, request, *args, **kwargs):
        task_conditions = request.session['task_conditions']
        print(f'task_data = {task_conditions}')
        task.apply_subject(**task_conditions)

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            return JsonResponse(
                data={
                    'question_text': task.question_text,
                    'answer_text': task.answer_text,
                    'timeout': task_conditions['timeout'],
                },
                status=200,
            )
        else:
            return render(request, 'task/common_demo.html')


class MathSolutionsView(TemplateView):
    """Mathematical tasks requiring answering view."""

    template_name = 'task/math_solutions.html'

    def get_context_data(self, **kwargs):
        """Add form to context."""
        context = super().get_context_data()
        context['form'] = NumberInputForm()
        return context

    def post(self, request):
        """Send task data to page and check user answer."""
        form = NumberInputForm(request.POST)
        answer_text = request.session.get('answer_text')

        if form.is_valid():
            user_solution = str(form.cleaned_data.get('user_solution'))

            if user_solution == answer_text:
                msg = 'Верно!'
                is_correct_solution = True
                data = {
                    'msg': msg,
                    'is_correct_solution': is_correct_solution,
                }
                return JsonResponse(data, status=200)
            else:
                msg = 'Не верно!'
                is_correct_solution = False
                data = {
                    'msg': msg,
                    'is_correct_solution': is_correct_solution,
                }
                return JsonResponse(data, status=200)

        return JsonResponse(data={}, status=200)


def render_task(request):
    """Send task data to page."""
    task_conditions = request.session['task_conditions']
    task.apply_subject(**task_conditions)
    request.session['answer_text'] = task.answer_text

    data = {
        'question_text': task.question_text,
    }
    return JsonResponse(data, status=200)
