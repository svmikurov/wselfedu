from django.forms import ModelForm

from english.models import CategoryModel


class CategoryForm(ModelForm):
    class Meta:
        model = CategoryModel
        fields = ('name',)
