"""Language discipline category CRUD views."""

from django.urls import reverse_lazy

from apps.core import views as core_views

from ..forms import CategoryForm
from ..models import Category

__all__ = [
    'CategoryListView',
    'CategoryCreateView',
    'CategoryUpdateView',
    'CategoryDeleteView',
]


class CategoryListView(core_views.BaseListView[Category]):
    """Category list view."""

    template_name = 'lang/category/index.html'
    context_object_name = 'categories'
    model = Category
    paginate_by = 15


class CategoryCreateView(core_views.BaseCreateView):
    """Category create view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:category_list')
    form_class = CategoryForm


class CategoryUpdateView(core_views.BaseUpdateView[Category]):
    """Category update view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:category_list')
    model = Category
    form_class = CategoryForm


class CategoryDeleteView(core_views.HtmxOwnerDeleteView):
    """Category delete view."""

    model = Category
