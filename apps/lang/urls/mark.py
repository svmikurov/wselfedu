"""English discipline mark url paths."""

from django.urls import path

from ..views import mark

urlpatterns = [
    path(
        'mark/list/',
        mark.MarkListView.as_view(),
        name='mark_list',
    ),
    path(
        'mark/create/',
        mark.MarkCreateView.as_view(),
        name='mark_create',
    ),
    path(
        'mark/<int:pk>/update/',
        mark.MarkUpdateView.as_view(),
        name='mark_update',
    ),
    path(
        'mark/<int:pk>/delete/',
        mark.MarkDeleteView.as_view(),
        name='mark_delete',
    ),
]
