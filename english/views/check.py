from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from english.tasks.study_words import get_random_sequence_language_keys
from english.tasks.test_task import TestWordTask

SUPERTITLE = 'Английский язык'
TITLE = 'Тест'
SUBTITLE = ''
COUNT_TO_ADD = 1.0
RIGHT_ANSWER_MESSAGE = 'Верно!'
WRONG_ANSWER_MESSAGE = 'Не верно!'


class TestWordView(
    TestWordTask,
    View,
):
    template_name = 'eng/tasks/test_word.html'

    def get(self, request):
        random_word, words_for_choice = self.create_task()
        task_language, answer_language = get_random_sequence_language_keys()
        request.session['random_word'] = random_word

        # if request.user.is_authenticated:
        #     user_id = request.user
        #     balance_by_today = get_user_data_by_today(
        #         user_id,
        #     ).get('balance')
        # else:
        #     balance_by_today = ''

        context = {
            'supertitle': SUPERTITLE,
            'title': TITLE,
            # 'balance_by_today': balance_by_today,
            'btn_name': 'Ответить',

            'random_word': random_word,
            'words_for_choice': words_for_choice,
            'task_language': task_language,
            'answer_language': answer_language,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        if 'choice' not in request.POST:
            return redirect(reverse_lazy('eng:test'))

        user_answer = request.POST['choice']
        correct_answer = request['correct_answer']

        # if request.user.is_authenticated:
        #     count_to_add = COUNT_TO_ADD
        # else:
        #     count_to_add = 0.0

        # if request.user.is_authenticated:
        #     add_vocabulary_user_answer_to_db(
        #         {
        #             'user_id': request.user.pk,
        #             'answer_word_id': int(user_answer),
        #             'task_word_id': correct_answer.get('id'),
        #         }
        #     )

        error_message = (
            f'{WRONG_ANSWER_MESSAGE} '
            f'*{correct_answer.get("task_word")}* переводится как '
            f'*{correct_answer.get("answer_word")}*')

        if str(user_answer) == str(correct_answer.get('id')):
            # if request.user.is_authenticated:
            #     add_count_to_user_balance(request.user, count_to_add)
            messages.success(request, RIGHT_ANSWER_MESSAGE)
        else:
            messages.error(request, error_message)

        return redirect(reverse_lazy('eng:test'))
