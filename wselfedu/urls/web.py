"""Defines application WEB URL paths."""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', include('apps.users.urls', namespace='users')),
    path('math/', include('apps.math.urls', namespace='math')),
]
