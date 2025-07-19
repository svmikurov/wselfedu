"""Contains project url paths."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('wselfedu.urls.web')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('wselfedu.urls.api_auth')),
    path('api/v1/', include('wselfedu.urls.api_v1')),
    path('docs/', include('wselfedu.urls.docs')),
]
