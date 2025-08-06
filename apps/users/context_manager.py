"""User application context processors."""

from typing import Any

from django.http import HttpRequest

from .models import Balance, Mentorship


def user_data(request: HttpRequest) -> dict[str, int | str]:
    """Add user data to template context."""
    context: dict[str, Any] = {}
    user_id = request.user.id

    # Mentorship
    user_has_mentor = Mentorship.objects.filter(student=user_id).exists()
    if user_has_mentor:
        balance = Balance.objects.filter(user_id=user_id).first()
        context.update(balance=balance or '-')

    return context
