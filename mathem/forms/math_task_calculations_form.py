from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML, ButtonHolder, Row, \
    Column
from django import forms
from django.urls import reverse_lazy


class MathTaskCalculationsForm(forms.Form):
    """Numeric answer entry form."""

    user_answer = forms.DecimalField(
        max_digits=5,
        required=True,
        label='',
        widget=forms.NumberInput(
            attrs={
                'style': "font-size: 3rem",
                'class': "text-center w-25 p-2",
            }
        )
    )

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_action = reverse_lazy('mathem:math_task_calculations')
        helper.form_method = 'post'
        helper.form_id = 'task_ajax'

        helper.layout = Layout(
            HTML("""
            <div class='text-center h1' id='evaluate'>{{ evaluate }}</div>
            """),
            HTML("""
            <div class='text-center h1' id='task_text'>{{ task_text }}</div>
            """),
            Row(
                Column(
                    Field('user_answer', css_class='text-center'),
                ),
            ),
            ButtonHolder(
                Submit('submit', 'Ответить', css_class='btn'),
                css_class='text-center'
            ),
        )

        return helper
