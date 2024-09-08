"""REST views."""

from rest_framework import generics

from glossary.models import Glossary
from glossary.serializers import GlossarySerializer


class GlossaryListAPIView(generics.ListCreateAPIView):
    """Create and List Glossary API view."""

    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer
