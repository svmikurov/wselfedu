"""Test the glossary exercise view."""

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from glossary.models import Glossary
from users.models import UserApp


class TestGlossaryExerciseView(APITestCase):
    """Test the Glossary exercise view.

    Test
    :py:meth:`task.views.glossary_exercise_drf_views.glossary_exercise`
    """

    def setUp(self) -> None:
        """Set up test data."""
        self.api_client = APIClient()
        self.user = UserApp.objects.create_user(username='user')
        self.url = reverse('glossary_rest:exercise')

    def test_http_status_200(self) -> None:
        """Test http status 200."""
        Glossary.objects.create(user=self.user, term='term')
        self.api_client.force_authenticate(self.user)
        r = self.api_client.post(self.url)
        assert r.status_code == status.HTTP_200_OK

    def test_http_status_400(self) -> None:
        """Test http status 400."""
        self.api_client.force_authenticate(self.user)
        r = self.api_client.post(self.url)
        assert r.status_code == status.HTTP_400_BAD_REQUEST
