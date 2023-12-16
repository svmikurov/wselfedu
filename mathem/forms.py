from django import forms


class UserAnswerForm(forms.Form):

    user_answer = forms.DecimalField(
        max_digits=4,
        label='Введи свой ответ',
    )
