"""URL configuration for wselfedu project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),  # noqa: E501
    path('users/', include('users.urls')),
    path('foreign/', include('foreign.urls.urls')),
    path('glossary/', include('glossary.urls.urls')),
    path('math/', include('mathematics.urls')),
]  # fmt: skip

# Mobile chapter urlpatterns.
mobile_urlpatterns = [
    path(
        'mobile/',
        TemplateView.as_view(template_name='mobile/main.html'),
        name='mobile_main',
    ),
    path(
        'mobile/install/',
        TemplateView.as_view(template_name='mobile/install.html'),
        name='mobile_install',
    ),
    path(
        'mobile/exercise/',
        TemplateView.as_view(template_name='mobile/exercise.html'),
        name='mobile_exercise',
    ),
]

# Django REST urlpatterns.
rest_urlpatterns = [
    path('api/v1/foreign/', include('foreign.urls.urls_rest')),
    path('api/v1/glossary/', include('glossary.urls.urls_rest')),
]

# Urlpatterns of installed packages.
packages_urlpatterns = [
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('captcha/', include('captcha.urls')),
]

urlpatterns += mobile_urlpatterns
urlpatterns += rest_urlpatterns
urlpatterns += packages_urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
