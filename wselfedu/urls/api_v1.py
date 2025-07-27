"""Defines apps api v1 url paths."""

from django.urls import include, path

from apps.lang.api.v1.urls import router as lang_router
from apps.main.api.v1.urls import router as main_router
from apps.math.api.v1.urls import router as math_router
from apps.users.api.v1.urls import router as users_router

urlpatterns = [
    path('lang/', include(lang_router.urls)),
    path('main/', include(main_router.urls)),
    path('math/', include(math_router.urls)),
    path('users/', include(users_router.urls)),
]
