"""Defines authentication URL paths for REST API."""

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # JWT
    path(
        'jwt/obtain/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'jwt/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path(
        'jwt/verify/',
        jwt_views.TokenVerifyView.as_view(),
        name='token_verify',
    ),
]
