"""English discipline category CRUD url paths."""

from django.urls import path

from ..views import category

urlpatterns = [
    path(
        'category/list/',
        category.CategoryListView.as_view(),
        name='category_list',
    ),
    path(
        'category/create/',
        category.CategoryCreateView.as_view(),
        name='category_create',
    ),
    path(
        'category/<int:pk>/update/',
        category.CategoryUpdateView.as_view(),
        name='category_update',
    ),
    path(
        'category/<int:pk>/delete/',
        category.CategoryDeleteView.as_view(),
        name='category_delete',
    ),
]
