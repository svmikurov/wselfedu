"""Calculate exercise views."""

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBase,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import RedirectView, TemplateView

from contrib.exercise.base import create_task, handel_answer
from mathematics.exercise.calculation import CalcExerciseBrowser
from mathematics.forms.calculate_choice import CalculationChoiceForm
from mathematics.forms.number_input import NumberInputForm
from users.models.points import get_points_balance


class MathCalculateChoiceView(TemplateView):
    """Select params math calculation task view."""

    template_name = 'mathematics/math_calculate_choice.html'
    form = CalculationChoiceForm

    def get(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponseRedirect | HttpResponse:
        """Check form view."""
        form = self.form(request.GET, request=request)

        if form.is_valid():
            task_conditions = form.clean()
            with_solution = task_conditions.pop('with_solution')
            request.session['task_conditions'] = task_conditions

            if with_solution:
                return redirect(reverse_lazy('math:math_calculate_solution'))
            else:
                return redirect(reverse_lazy('math:math_calculate_demo'))

        context = {
            'title': 'Условия задания',
            'form': self.form(request=request),
        }
        return render(request, self.template_name, context)


class MathCalculateDemoView(View):
    """Math calculation demonstration view.

    The user is shown a mathematical expression as a question. The user
    calculates the mathematical expression. After a timeout, the user
    is shown the result of the mathematical expression. The user
    compares his calculation with the result of the mathematical
    expression displayed on the page.
    """

    template_name = 'mathematics/math_calculate_demo.html'

    def get(self, request: HttpRequest) -> JsonResponse | HttpResponse:
        """Render the task page and update tasks later on the page."""
        task_conditions = request.session['task_conditions']
        task = CalcExerciseBrowser(**task_conditions)

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
    """Calculate exercise view with input of a solution and scoring."""

    template_name = 'mathematics/math_calculate_solution.html'

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add form with title to context."""
        context = super().get_context_data()
        context['form'] = NumberInputForm()
        context['title'] = 'Вычисления с вводом ответа'
        return context

    def post(self, request: HttpRequest) -> JsonResponse:
        """Accept user's answer for verification."""
        form = NumberInputForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            answer = {'answer': str(data.get('user_solution'))}
            is_correctly = handel_answer(answer, request.user)

            return JsonResponse(
                data={
                    'msg': 'Верно!' if is_correctly else 'Неверно!',
                    'is_correct_solution': is_correctly,
                },
                status=200,
            )

        return JsonResponse(data={}, status=200)


def render_task(request: HttpRequest) -> JsonResponse:
    """Send question text to page."""
    exercise_conditions = request.session.get('task_conditions')
    exercise_conditions.pop('timeout')
    task = create_task(exercise_conditions, request.user)
    balance = get_points_balance(request.user.id) / 100

    return JsonResponse(
        data={
            'success': True,
            'question_text': task.data_to_render['question'],
            'balance': balance,
        },
        status=200,
    )


class SetMultiplicationTableExerciseView(RedirectView):
    """Setup initial data for multiplication table exercises view.

    Saves to session the ``task_conditions``.

    Redirect to ``MathCalculateSolutionView``.
    """

    url = reverse_lazy('math:math_calculate_solution')

    def get(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponseBase:
        """Save task conditions in session."""
        task_conditions = {
            'calculation_type': 'mul',
            'min_value': 2,
            'max_value': 9,
        }
        request.session['task_conditions'] = task_conditions
        response = super().get(request, *args, **kwargs)
        return response
