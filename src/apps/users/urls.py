"""Users application urls."""

from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'signup',
        views.SignUpView.as_view(),
        name='signup',
    ),
    path(
        'profile/<slug:username>/',
        views.ProfileView.as_view(),
        name='profile',
    ),
    path(
        'profile/edit/<slug:username>/',
        views.ProfileEditView.as_view(),
        name='profile-edit',
    ),
]
