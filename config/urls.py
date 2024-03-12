import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import FormCrispyView
from config.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('users/', include('users.urls')),
    path('math/', include('mathem.urls')),
    path('english/', include('english.urls')),
    path('django-crispy-filter/', FormCrispyView.as_view(), name='form_crispy'),
]

if os.getenv('ENVIRONMENT') != 'PRODUCTION':
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
