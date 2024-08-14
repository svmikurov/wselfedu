from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from task.forms import MathCalculationChoiceForm, NumberInputForm
from task.points import get_points_balance
from task.task_mng import CalculationExerciseCheck
from task.tasks.calculation_exersice import CalculationExercise


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
    """Calculate exercise view with input of a solution and scoring.

    The ``get`` method renders the page for the exercise.
    The page contains a form for entering the user's solution.

    On the user side, a post-request is generated via Ajax to receive
    the task.

    The ``post`` method accepts a user response for validation and
    returns a JSON response with an evaluate.
    """

    template_name = 'task/mathem/math_calculate_solution.html'

    def get_context_data(self, **kwargs):
        """Add form with title to context."""
        context = super().get_context_data()
        context['form'] = NumberInputForm()
        context['title'] = 'Вычисления с вводом ответа'
        return context

    def post(self, request):
        """Accept user's answer for verification."""
        form = NumberInputForm(request.POST)

        if form.is_valid():
            task_mgr = CalculationExerciseCheck(request=request, form=form)
            is_correct_solution: bool = task_mgr.check_and_save_user_solution()
            msg = 'Верно!' if is_correct_solution else 'Неверно!'

            return JsonResponse(
                data={
                    'msg': msg,
                    'is_correct_solution': is_correct_solution,
                },
                status=200,
            )

        return JsonResponse(data={}, status=200)


def render_task(request: HttpRequest) -> JsonResponse:
    """Send question text to page.

    Gets the task creation conditions from the session.
    Create new ``task`` instance, save ``answer_text`` in session,
    render new ``question_text`` to user via json response.

    Parameters
    ----------
    request : `HttpRequest`
        Request to receive new text of the question.


    Return
    ------
    `JsonResponse`
        Json response with new question text.

    """
    task_conditions = request.session.get('task_conditions')
    if not task_conditions:
        redirect(reverse_lazy('task:math_calculate_choice'))

    user_id = request.user.id
    # A new task is created when the class CalculationExercise
    # is initialized.
    task = CalculationExercise(user_id=user_id, **task_conditions)
    request.session['calculation_type'] = task.calculation_type
    request.session['question_text'] = task.question_text
    request.session['answer_text'] = task.answer_text

    return JsonResponse(
        data={
            'success': True,
            'question_text': task.question_text,
            'balance': get_points_balance(user_id),
        },
        status=200,
    )
