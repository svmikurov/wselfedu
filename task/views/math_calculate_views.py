from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from jsonview.decorators import json_view

from task.forms import MathCalculationChoiceForm, NumberInputForm
from task.tasks.math_calculate_task import CalculationExercise


class MathCalculateChoiceView(TemplateView):
    """Select params math calculation task view."""

    template_name = 'task/mathem/math_calculate_choice.html'
    form = MathCalculationChoiceForm

    def get(self, request, *args, **kwargs):
        form = self.form(request.GET, request=request)

        if form.is_valid():
            task_conditions = form.clean()
            with_solution = task_conditions.pop('with_solution')
            request.session['task_conditions'] = task_conditions

            if with_solution:
                return redirect(reverse_lazy('task:math_calculate_solution'))
            else:
                return redirect(reverse_lazy('task:math_calculate_demo'))

        context = {
            'title': 'Условия задания',
            'form': self.form(request=request),
        }
        return render(request, self.template_name, context)


class MathCalculateDemoView(View):
    """Math calculation demonstration view."""

    template_name = 'task/mathem/math_calculate_demo.html'

    def get(self, request, *args, **kwargs):
        """Render the task page and update tasks later on the page."""
        task_conditions = request.session['task_conditions']
        task = CalculationExercise(**task_conditions)

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data = {
                'question_text': task.question_text,
                'answer_text': task.answer_text,
                'timeout': task.timeout,
            }
            return JsonResponse(data=data, status=200)

        context = {
            'title': 'Задание на вычисление',
        }
        return render(request, self.template_name, context)


class MathCalculateSolutionView(TemplateView):
    """Math tasks requiring answering view."""

    template_name = 'task/mathem/math_calculate_solution.html'

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
                return JsonResponse(
                    data={
                        'msg': 'Верно!',
                        'is_correct_solution': True,
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    data={
                        'msg': 'Неверно!',
                        'is_correct_solution': False,
                    },
                    status=200,
                )

        return JsonResponse(data={}, status=200)


@json_view
def render_task(request):
    """Send task data to page."""
    task_conditions = request.session['task_conditions']
    task = CalculationExercise(**task_conditions)
    request.session['answer_text'] = task.answer_text
    data = {
        'success': True,
        'question_text': task.question_text,
    }
    return data
