from django.urls import path

from wselfedu.users import views

app_name = 'user'
urlpatterns = [
    path(
        'registration/',
        views.UserRegistrationView.as_view(template_name='form.html'),
        name='create',
    ),
]
