"""URL configuration for project."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_urlpatterns = [
    path('api/v1/users', include('apps.users.api.v1.urls')),
]

web_urlpatterns = [
    path('', include('apps.main.urls')),
    path('users/', include('apps.users.urls')),
]

urlpatterns = (
    [
        path('admin/', admin.site.urls),
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.jwt')),
        path(
            'api/schema/',
            SpectacularAPIView.as_view(),
            name='schema',
        ),
        path(
            'api/schema/swagger-ui/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui',
        ),
        path(
            'api/schema/redoc/',
            SpectacularRedocView.as_view(url_name='schema'),
            name='redoc',
        ),
    ]
    + api_urlpatterns
    + web_urlpatterns
)
