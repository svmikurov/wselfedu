from django.forms import ModelForm

from english.models import SourceModel


class SourceForm(ModelForm):

    class Meta:
        model = SourceModel
        fields = ('name', 'url')
