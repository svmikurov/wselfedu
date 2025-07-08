"""Defines Users application API view."""

from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets

from apps.users.api.v1.serializers import (
    GroupSerializer,
    UserSerializer,
)
from apps.users.models import CustomUser


class UserViewSet(viewsets.ModelViewSet):  # type: ignore[type-arg]
    """API endpoint that allows users to be viewed or edited."""

    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class GroupViewSet(viewsets.ModelViewSet):  # type: ignore[type-arg]
    """API endpoint that allows groups to be viewed or edited."""

    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]
