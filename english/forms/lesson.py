from django.forms import ModelForm

from english.models import LessonModel


class LessonForm(ModelForm):

    class Meta:
        model = LessonModel
        fields = ['name']
