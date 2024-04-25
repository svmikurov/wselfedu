from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from contrib_app.task import calculation_subject
from mathem.forms.math_calculations_task_form import MathTaskCommonSelectForm


class SelectMathTaskParamsView(TemplateView):
    """Select params task view."""

    template_name = 'mathem/math_calculations_select.html'

    def get(self, request, *args, **kwargs):
        completed_form = MathTaskCommonSelectForm(request.GET)

        if completed_form.is_valid():
            task_data = completed_form.clean()
            task_data['min_value'] = int(task_data['min_value'])
            task_data['max_value'] = int(task_data['max_value'])
            task_data['timeout'] = int(task_data['timeout'])
            task_data['subject_name'] = calculation_subject.subject_name

            request.session['task_data'] = task_data
            return redirect(reverse_lazy('common_task_interface'))

        context = {
            'form': MathTaskCommonSelectForm
        }
        return render(request, self.template_name, context)
