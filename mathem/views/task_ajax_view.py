from django.http import JsonResponse
from django.views.generic import TemplateView

from mathem.core.base import TwoOperandMathTask
from mathem.forms.calculations_form_ajax import CalculationAjaxForm


class TaskAjax(TemplateView):

    template_name = 'mathem/calculations_ajax.html'
    form = CalculationAjaxForm()
    task = TwoOperandMathTask(1, 30, '+')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['task_text'] = self.task
        context['form'] = self.form
        return context

    def post(self, request):
        user_answer = request.POST.get('user_answer')

        if self.task.evaluate_solution(user_answer):
            return JsonResponse(
                data={
                    'evaluate': 'Верно!',
                    'task_text': self.task()
                },
                status=201
            )
        else:
            return JsonResponse(
                data={
                    'evaluate': 'Не верно!',
                },
                status=201
            )
