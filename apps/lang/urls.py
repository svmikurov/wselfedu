"""Language discipline web urls paths."""

from django.urls import path

from . import views

app_name = 'lang'

urlpatterns = [
    path('', views.IndexLangView.as_view(), name='index'),
    path(
        'label/create/',
        views.LabelCreateView.as_view(),
        name='label_create',
    ),
    path(
        'label/<int:pk>/update/',
        views.LabelUpdateView.as_view(),
        name='label_update',
    ),
    path(
        'label/<int:pk>/delete/',
        views.LabelDeleteView.as_view(),
        name='label_delete',
    ),
    path(
        'label/<int:pk>/',
        views.LabeDetailView.as_view(),
        name='label_detail',
    ),
    path(
        'label/list/',
        views.LabelListView.as_view(),
        name='label_list',
    ),
]
