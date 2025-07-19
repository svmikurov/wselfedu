"""Defines apps api v1 url paths."""

from django.urls import include, path

from apps.math.api.v1.urls import router as math_router
from apps.users.api.v1.urls import router as users_router

urlpatterns = [
    path('main/', include(users_router.urls)),
    path('users/', include(users_router.urls)),
    path('math/', include(math_router.urls)),
]
