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
            form_data = completed_form.clean()
            form_data['min_value'] = int(form_data['min_value'])
            form_data['max_value'] = int(form_data['max_value'])

            request.session['subject_name'] = calculation_subject.subject_name
            request.session['subject_attrs'] = form_data
            return redirect(reverse_lazy('common_task_interface'))

        context = {
            'form': MathTaskCommonSelectForm
        }
        return render(request, self.template_name, context)
