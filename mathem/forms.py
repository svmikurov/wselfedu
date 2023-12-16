from django import forms


class UserAnswerForm(forms.Form):

    user_answer = forms.CharField(
        max_length=4,
        label='Введи свой ответ',
    )
