"""URL configuration for settings project."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wse.site.core.urls')),
]
