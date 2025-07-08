"""Defines application API URL paths."""

from django.urls import include, path

from apps.math.api.v1.urls import router as math_router
from apps.users.api.v1.urls import router as users_router

urlpatterns = [
    path('users/', include(users_router.urls)),
    path('math/', include(math_router.urls)),
]
