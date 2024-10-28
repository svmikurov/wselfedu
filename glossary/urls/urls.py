"""Glossary app DRF urls."""

from django.urls import path
from django.views.generic import TemplateView

from glossary import views

app_name = 'glossary'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='glossary/home.html'),
        name='home',
    ),
    path(
        'term-create/',
        views.TermCreateView.as_view(),
        name='term_create',
    ),
    path(
        'term-list/',
        views.TermListView.as_view(),
        name='term_list',
    ),
    path(
        'term-ditail/<int:pk>/',
        views.TermDitailView.as_view(),
        name='term_detail',
    ),
    path(
        'params/',
        TemplateView.as_view(template_name='glossary/params.html'),
        name='params',
    ),
]

category_paths = [
    path(
        'category/create',
        views.CategoryCreateView.as_view(),
        name='category_create',
    ),
    path(
        'category/list',
        views.CategoryListView.as_view(),
        name='category_list',
    ),
    path(
        'category/update/<int:pk>/',
        views.CategoryUpdateView.as_view(),
        name='category_update',
    ),
    path(
        'category/delete/<int:pk>/',
        views.CategoryDeleteView.as_view(),
        name='category_delete',
    ),
]

source_paths = [
    path(
        '/create',
        views.SourceCreateView.as_view(),
        name='source_create',
    ),
    path(
        'source/list',
        views.SourceListView.as_view(),
        name='source_list',
    ),
    path(
        'source/update/<int:pk>/',
        views.SourceUpdateView.as_view(),
        name='source_update',
    ),
    path(
        'source/delete/<int:pk>/',
        views.SourceDeleteView.as_view(),
        name='source_delete',
    ),
]

urlpatterns += category_paths
urlpatterns += source_paths
