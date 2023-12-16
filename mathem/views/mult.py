from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from mathem.forms import UserAnswerForm
from mathem.tasks.mult import MultTask

SUCCESS_MESSAGE = 'Верно!'
ERROR_MESSAGE = 'Не верно!'


class MultTaskView(MultTask, View):
    """
    View of a multiplication task.
    Task data is stored in the session.
    """

    template_name = 'mathem/mult.html'
    context = {'title': 'Таблица умножения'}

    def get(self, request, *args, **kwargs):
        """Create task."""
        form = UserAnswerForm()
        text_task, correct_answer = self.create_task()
        request.session['text_task'] = text_task
        request.session['correct_answer'] = correct_answer
        self.context.update({'form': form, 'text_task': text_task})
        return render(request, self.template_name, self.context)

    def post(self, request):
        """Check user answer"""
        form = UserAnswerForm(request.POST)
        text_task = request.session['text_task']
        correct_answer = request.session['correct_answer']

        if form.is_valid():
            user_answer = form.cleaned_data.get('user_answer')
            if str(user_answer) == str(correct_answer):
                messages.success(request, SUCCESS_MESSAGE)
                return redirect(reverse_lazy('math:mult'))

        # Repeats the question
        # if the answer is incorrect or the answer is not above
        messages.error(request, ERROR_MESSAGE)
        self.context.update({'form': form, 'text_task': text_task})
        return render(request, self.template_name, self.context)
