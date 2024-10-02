"""URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please
see: https://docs.djangoproject.com/en/4.2/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include,
       path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from foreign.views.drf import (
    WordDetailAPIView,
    WordListCreateAPIView,
)
from glossary.views.exercise import (
    glossary_exercise,
    glossary_exercise_parameters,
    update_term_study_progress,
)
from glossary.views.glossary import (
    GlossaryDetailAPIView,
    GlossaryListAPIView,
)

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('users.urls')),
    path('foreign/', include('foreign.urls')),
    path('math/', include('mathematics.urls')),
]

drf_urlpatterns = [
    # Session auth
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    # Token auth
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # End Auth
    # Word
    path(
        'api/v1/word/<int:pk>/',
        WordDetailAPIView.as_view(),
        name='api-word',
    ),
    path(
        'api/v1/word/',
        WordListCreateAPIView.as_view(),
        name='api-words',
    ),
    # Glossary
    path(
        'api/v1/glossary/<int:pk>/',
        GlossaryDetailAPIView.as_view(),
        name='api_term',
    ),
    path(
        'api/v1/glossary/',
        GlossaryListAPIView.as_view(),
        name='api_glossary',
    ),
    path(
        'api/v1/glossary/progress/',
        update_term_study_progress,
        name='api_glossary_term_progress',
    ),
    path(
        'api/v1/glossary/exercise/',
        glossary_exercise,
        name='api_glossary_exercise',
    ),
    path(
        'api/v1/glossary/exercise/parameters/',
        glossary_exercise_parameters,
        name='api_glossary_exercise_parameters',
    ),
]

urlpatterns += drf_urlpatterns
