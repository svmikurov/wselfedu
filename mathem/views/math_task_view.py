from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from mathem.core.base_not_call_ import TwoOperandMathTaskNotCall
from mathem.forms import MathTaskChoiceForm, MathTaskCalculationsForm


class MathTaskChoiceView(TemplateView):
    """"""

    template_name = 'mathem/math_task_choice.html'
    form = MathTaskChoiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request):
        """Get from user form task data.
        """
        form = MathTaskChoiceForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            task_data = dict()

            task_data['min_value'] = int(form_data['min_value'])
            task_data['max_value'] = int(form_data['max_value'])
            task_data['ops'] = form_data['calculation_type']

            request.session['task_data'] = task_data
            return redirect(reverse_lazy('mathem:math_task_calculations'))

        return render(request, self.template_name, {'form': form})


class MathTaskCalculationsView(TemplateView):
    """"""

    template_name = 'mathem/form_crispy.html'
    form = MathTaskCalculationsForm

    def get_context_data(self, **kwargs):
        task_data = self.request.session['task_data']
        task = TwoOperandMathTaskNotCall(**task_data)
        task_text = task.create_task()
        calculation = task.get_calculation()

        self.request.session['calculation'] = calculation

        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['task_text'] = task_text

        return context

    def post(self, request):
        """"""
        calculation = request.session['calculation']
        user_answer = request.POST.get('user_answer')

        if int(calculation) == int(user_answer):
            task_data = self.request.session['task_data']
            task = TwoOperandMathTaskNotCall(**task_data)
            task_text = task.create_task()
            calculation = task.get_calculation()
            request.session['calculation'] = calculation

            return JsonResponse(
                data={
                    'evaluate': 'Верно!',
                    'task_text': task_text
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
