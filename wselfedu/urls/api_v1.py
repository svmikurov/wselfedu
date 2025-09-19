"""Defines apps api v1 url paths."""

from django.urls import include, path

from apps.core.api.v1.urls import router as core_router
from apps.glossary.api.v1.urls import router as terms_router
from apps.math.api.v1.urls import router as math_router
from apps.study.api.v1.urls import router as study_router
from apps.users.api.v1.urls import router as users_router

urlpatterns = [
    path('core/', include((core_router.urls, 'core'), namespace='core')),
    path('math/', include((math_router.urls, 'math'), namespace='math')),
    path('study/', include((study_router.urls, 'study'), namespace='study')),
    path('users/', include(users_router.urls)),
    path(
        'glossary/',
        include((terms_router.urls, 'glossary_api'), namespace='glossary_api'),
    ),
]
