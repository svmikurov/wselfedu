"""Language discipline category CRUD views."""

from django.urls import reverse_lazy

from apps.core.views import crud

from ..forms import CategoryForm
from ..models import Category

__all__ = [
    'CategoryListView',
    'CategoryCreateView',
    'CategoryUpdateView',
    'CategoryDeleteView',
]


class CategoryListView(crud.BaseListView[Category]):
    """Category list view."""

    template_name = 'lang/category/index.html'
    context_object_name = 'categories'
    paginate_by = 15
    model = Category


class CategoryCreateView(crud.BaseCreateView):
    """Category create view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:category_list')
    form_class = CategoryForm


class CategoryUpdateView(crud.BaseUpdateView[Category]):
    """Category update view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:category_list')
    form_class = CategoryForm
    model = Category


class CategoryDeleteView(crud.HtmxOwnerDeleteView):
    """Category delete view."""

    model = Category
