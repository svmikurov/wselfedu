from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from task.forms import EnglishTranslationChoiceForm
from task.task import task, translate_subject


class EnglishTranslationChoiceView(TemplateView):
    """"""

    template_name = 'task/english/english_translation_choice.html'
    task_subject = translate_subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Выберите условия задания'
        context['form'] = EnglishTranslationChoiceForm(request=self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = EnglishTranslationChoiceForm(request.POST, request=request)

        if form.is_valid():
            task_conditions = form.clean()
            task_conditions['subject_name'] = self.task_subject.subject_name
            request.session['task_conditions'] = task_conditions

            return redirect(reverse_lazy('task:english_translation_demo'))

        return render(request, self.template_name, {'form': form})


class EnglishTranslationDemoView(TemplateView):
    """"""

    template_name = 'task/english/english_translation_demo.html'
    extra_context = {
        'title': {
            'title_name': 'Изучаем слова',
            'url_name': 'task:english_translation_choice',
        }
    }

    def post(self, request):
        """"""
        task_conditions = request.session['task_conditions']
        task.apply_subject(**task_conditions)

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        data = {
            'question_text': task.question_text,
            'answer_text': task.answer_text,
            'info': task.info,
            'timeout': task_conditions['timeout'],
        }
        print(data)
        if is_ajax:
            return JsonResponse(
                data=data,
                status=200,
            )
