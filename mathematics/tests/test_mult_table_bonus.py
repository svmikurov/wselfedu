"""Test task manager module."""

from django.test import TestCase
from django.urls import reverse_lazy

from users.models import UserApp


class TestMultTableForBonus(TestCase):
    """Test task manager class."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = UserApp.objects.create(username='user')

    def test_start_table_mult_exercise(self) -> None:
        """Test redirect to exercise."""
        url_start_exercise = reverse_lazy('math:math_set_table_mult_points')
        redirect_url = reverse_lazy('math:math_calculate_solution')
        self.client.force_login(self.user)
        response = self.client.get(url_start_exercise)

        self.assertRedirects(response, redirect_url, 302)
