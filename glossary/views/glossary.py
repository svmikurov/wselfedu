"""Glossary views."""

from django.db.models import QuerySet
from rest_framework import generics, permissions

from contrib.views_rest import IsOwner
from glossary.models import Glossary
from glossary.serializers import GlossarySerializer


class GlossaryListCreateAPIView(generics.ListCreateAPIView):
    """Create and List Glossary API view."""

    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer


class GlossaryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and destroy Glossary API view."""

    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer
