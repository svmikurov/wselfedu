"""Defines apps api v1 url paths."""

from django.urls import include, path

from apps.core.api.v1.urls import router as core_router
from apps.lang.api.v1.urls import router as lang_router
from apps.math.api.v1.urls import router as math_router
from apps.users.api.v1.urls import router as users_router

urlpatterns = [
    path('lang/', include(lang_router.urls)),
    path('core/', include(core_router.urls)),
    path('math/', include(math_router.urls)),
    path('users/', include(users_router.urls)),
]
