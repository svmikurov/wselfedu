from django.urls import path

from wselfedu.users import views

app_name = 'user'
urlpatterns = [
    path(
        'registration/',
        views.UserRegistrationView.as_view(template_name='form.html'),
        name='create',
    ),
    path(
        '<pk>/account/',
        views.UserDetailView.as_view(template_name='users/account.html'),
        name='detail',
    ),
]
