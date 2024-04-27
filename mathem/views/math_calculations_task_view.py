from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from task.task import calculation_subject
from mathem.forms.math_calculations_task_form import MathTaskCommonSelectForm


class SelectMathTaskParamsView(TemplateView):
    """Select params task view."""

    template_name = 'mathem/math_calculations_select.html'

    def get(self, request, *args, **kwargs):
        completed_form = MathTaskCommonSelectForm(request.GET, request=request)

        if completed_form.is_valid():
            task_conditions = completed_form.clean()
            task_conditions['subject_name'] = calculation_subject.subject_name
            with_solution = task_conditions.pop('with_solution')
            request.session['task_conditions'] = task_conditions

            if with_solution:
                return redirect(reverse_lazy('task:math_solutions'))
            else:
                return redirect(reverse_lazy('task:common_demo'))

        context = {
            'form': MathTaskCommonSelectForm(request=request),
        }
        return render(request, self.template_name, context)
