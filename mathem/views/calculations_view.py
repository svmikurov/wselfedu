from django.shortcuts import render
from django.views.generic import TemplateView

from mathem.core.base import TwoOperandMathTask
from mathem.forms.calculations_form import CalculationChoiceForm

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


def two_operand_math_task(request, *args, **kwargs):
    ...
