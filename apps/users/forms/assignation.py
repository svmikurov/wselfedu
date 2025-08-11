"""Defines forms for mentorship exercise."""

from crispy_forms.helper import (  # type: ignore[import-untyped]
    FormHelper,
    Layout,
)
from crispy_forms.layout import Submit  # type: ignore[import-untyped]
from django import forms
from django.urls import reverse

from apps.core.models.exercise import Exercise
from apps.core.orchestrators.exercise import ExerciseAssignator
from apps.users.models import Mentorship


class AssignExerciseForm(forms.Form):
    """Form for assign exercise in mentorship."""

    exercise = forms.ModelChoiceField(
        queryset=Exercise.objects.all().only('id', 'name'),
        required=True,
        empty_label='-',
        label='Упражнение',
    )
    count = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Количество',
    )
    award = forms.IntegerField(
        min_value=0,
        max_value=1000,
        initial=0,
        label='Вознаграждение',
        help_text='Размер вознаграждения за одно успешно '
        'выполненное задание (0-1000)',
    )
    is_active = forms.BooleanField(
        initial=False,
        required=False,
        label='Активно',
    )
    is_daily = forms.BooleanField(
        initial=False,
        required=False,
        label='Ежедневное',
    )
    expiration = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Срок выполнения',
    )

    def __init__(
        self,
        *args: object,
        mentorship: Mentorship | None = None,
        **kwargs: object,
    ) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        if not mentorship:
            raise ValueError('mentorship required')

        self.mentorship = mentorship
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        # HTMX
        self.helper.attrs = {
            'hx-post': reverse(
                'users:mentorship-mentor-student-assign',
                kwargs={'pk': mentorship.pk},
            ),
            'hx-target': '#assigned-exercises',
        }

        # Form style
        self.helper.form_class = 'form-horizontal form-control'
        self.helper.label_class = 'col-sm-4 col-md-3'
        self.helper.field_class = 'col-sm-6 col-md-5'

        # Form layout
        self.helper.layout = Layout(
            'exercise',
            'count',
            'award',
            'expiration',
            'is_daily',
            'is_active',
            Submit('submit', 'Назначить'),
        )

    def create(self) -> None:
        """Save exercise assignment."""
        orchestrator = ExerciseAssignator(
            self.mentorship,
        )
        orchestrator.create(self.cleaned_data)
