from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from task.forms import EnglishTranslateChoiceForm
from task.task import task, translate_subject


class EnglishTranslateChoiceView(TemplateView):
    """"""

    template_name = 'task/english/english_translate_choice.html'
    form = EnglishTranslateChoiceForm
    task_subject = translate_subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Выберите условия задания'
        context['form'] = self.form(request=self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request=request)

        if form.is_valid():
            task_conditions = form.clean()
            task_conditions['subject_name'] = self.task_subject.subject_name
            task_conditions['user_id'] = request.user.id
            request.session['task_conditions'] = task_conditions

            return redirect(reverse_lazy('task:english_translate_demo'))

        return render(request, self.template_name, {'form': self.form})


class EnglishTranslateDemoView(TemplateView):
    """"""

    template_name = 'task/english/english_translate_demo.html'
    extra_context = {
        'title': {
            'title_name': 'Изучаем слова',
            'url_name': 'task:english_translate_choice',
        },
    }

    def post(self, request):
        """"""
        task_conditions = request.session['task_conditions']
        task.apply_subject(**task_conditions)

        data = {
            'question_text': task.question_text,
            'answer_text': task.answer_text,
            'timeout': task_conditions['timeout'],
        }
        return JsonResponse(data, status=200)
