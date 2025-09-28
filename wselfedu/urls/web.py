"""Defines apps web url paths."""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from apps.users import views as users_views

urlpatterns = [
    path('', include('apps.core.urls')),
    path('signup/', users_views.SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('glossary/', include('apps.glossary.urls'), name='glossary'),
    path('lang/', include('apps.lang.urls'), name='lang'),
    # TODO: Add POST requests logout
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('apps.users.urls')),
]
