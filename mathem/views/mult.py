from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from mathem.forms import UserAnswerForm
from mathem.tasks.mult import MultTask

success_message = 'Верно!'
error_message = 'Не верно!'


class MultTaskView(MultTask, View):
    template_name = 'mathem/mult.html'
    context = {'title': 'Таблица умножения'}

    def get(self, request, *args, **kwargs):
        form = UserAnswerForm()
        text_task, correct_answer = self.create_task()
        request.session['text_task'] = text_task
        request.session['correct_answer'] = correct_answer
        self.context.update({'form': form, 'text_task': text_task})
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = UserAnswerForm(request.POST)
        text_task = request.session['text_task']
        correct_answer = request.session['correct_answer']
        data: dict = request.POST.dict()
        user_answer = data.get('user_answer')

        if form.is_valid():
            if str(user_answer) == str(correct_answer):
                messages.success(request, success_message)
                return redirect(reverse_lazy('math:mult'))
            else:
                messages.error(request, error_message)
                self.context.update({'form': form, 'text_task': text_task})
                return render(request, self.template_name, self.context)

        self.context.update({'form': form, 'text_task': text_task})
        return render(request, self.template_name, self.context)
