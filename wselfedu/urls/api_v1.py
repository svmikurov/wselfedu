"""Defines apps api v1 url paths."""

from django.urls import include, path

from apps.core.api.v1.urls import router as core_router
from apps.glossary.api.v1.urls import router as terms_router
from apps.lang.api.v1.urls import router as lang_router
from apps.math.api.v1.urls import router as math_router
from apps.study.api.v1.urls import router as study_router
from apps.users.api.v1.urls import router as users_router

# fmt: off
urlpatterns = [
    path('core/', include((core_router.urls, 'core'), namespace='core_api')),
    path('math/', include((math_router.urls, 'math'), namespace='math_api')),
    path('study/', include((study_router.urls, 'study'), namespace='study_api')),  # noqa: E501
    path('users/', include(users_router.urls)),
    path('glossary/', include((terms_router.urls, 'glossary'), namespace='glossary_api')),  # noqa: E501
    path('lang/', include((lang_router.urls, 'lang'), namespace='lang_api')),  # noqa: E501
]
# fmt: on
