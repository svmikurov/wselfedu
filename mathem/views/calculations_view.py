from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from mathem.core.base import TwoOperandMathTask
from mathem.forms.calculations_form import CalculationChoiceForm
from mathem.forms.calculations_form_ajax import CalculationAjaxForm

TITLE = {
    'add': 'Сложение',
    'sub': 'Вычитание',
    'mult': 'Умножение',
}
OPS = {
    'ADD': '+',
    'SUB': '-',
    'MUL': '*',
}


class CalculationsView(TemplateView):
    """Simple math exercises view."""

    template_name = 'mathem/calculations.html'
    form = CalculationChoiceForm()
    extra_context = {
        'title': 'Вычисления',
        'form': form,
    }

    def post(self, request, *args, **kwargs):
        form = CalculationChoiceForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data

            calculation_type = form['calculation_type']
            operations = OPS[calculation_type]
            min_value = int(form['min_value'])
            max_value = int(form['max_value'])

            task = TwoOperandMathTask(min_value, max_value, operations)
            form = CalculationChoiceForm(initial={'question_field': task})

        return render(request, self.template_name, {'form': form})


class TaskAjax(TemplateView):

    template_name = 'mathem/calculations_ajax.html'
    form = CalculationAjaxForm()
    task = TwoOperandMathTask(1, 10, '+')

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
