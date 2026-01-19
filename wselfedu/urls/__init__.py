"""Contains project url paths."""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('wselfedu.urls.api_auth')),
    path('api/v1/', include('wselfedu.urls.api_v1')),
    path('docs/', include('wselfedu.urls.docs')),
] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('wselfedu.urls.web')),
    prefix_default_language=False,
)

if settings.DEBUG:
    import debug_toolbar  # type: ignore[import-untyped]

    urlpatterns = [  # type: ignore[assignment]
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns  # type: ignore[operator]
