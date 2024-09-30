"""Glossary views."""

from django.http import HttpRequest, HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser

from config.constants import (
    ACTION,
    ID,
    POST,
    PROGRES_STEPS,
    PROGRESS,
    PROGRESS_MAX,
    PROGRESS_MIN,
)
from glossary.models import Glossary, GlossaryProgress
from glossary.serializers import GlossarySerializer


class GlossaryListAPIView(generics.ListCreateAPIView):
    """Create and List Glossary API view."""

    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer


class GlossaryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and destroy Glossary API view."""

    queryset = Glossary.objects.all()
    serializer_class = GlossarySerializer


@api_view([POST])
@permission_classes((permissions.AllowAny,))
def update_term_study_progress(request: HttpRequest) -> HttpResponse:
    """Update term study progres."""
    user = request.user
    payload = JSONParser().parse(request)
    term_pk = payload.get(ID)

    try:
        term = Glossary.objects.get(pk=term_pk)
    except Glossary.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    else:
        # Only owner have access to his term.
        if user != term.user:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

    obj, _ = GlossaryProgress.objects.get_or_create(term=term, user=user)
    action = payload.get(ACTION)
    progres_delta = PROGRES_STEPS.get(action)
    updated_progres = obj.progress + progres_delta

    if PROGRESS_MIN <= updated_progres <= PROGRESS_MAX:
        obj.progress = updated_progres
        obj.save(update_fields=[PROGRESS])

    return HttpResponse(status=status.HTTP_200_OK)
