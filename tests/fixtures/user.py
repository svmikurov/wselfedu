"""Users application fixtures."""

from unittest.mock import Mock

import pytest
from django.contrib.auth.models import AnonymousUser

from apps.users.models import Mentorship, Person

# ===============================================
# Database fixtures
# ===============================================


@pytest.fixture
def user() -> Person:
    """Provide user."""
    return Person.objects.create_user(username='user', password='pass')


# -----------------------------------------------
# Ownership
# -----------------------------------------------


@pytest.fixture
def owner() -> Person:
    """Provide owner of DB object."""
    return Person.objects.create_user(username='owner', password='pass')


@pytest.fixture
def not_owner() -> Person:
    """Provide user that is not the owner of DB object."""
    return Person.objects.create_user(username='not_owner', password='pass')


# -----------------------------------------------
# Mentorship
# -----------------------------------------------


@pytest.fixture
def mentorship() -> Mentorship:
    """Provide mentorship."""
    student = Person.objects.create_user(username='student', password='pass')
    mentor = Person.objects.create_user(username='mentor', password='pass')
    return Mentorship.objects.create(mentor=mentor, student=student)


@pytest.fixture
def student(mentorship: Mentorship) -> Person:
    """Provide student."""
    return mentorship.student


@pytest.fixture
def mentor(mentorship: Mentorship) -> Person:
    """Provide mentor."""
    return mentorship.mentor


# ===============================================
# Mock user fixtures
# ===============================================


@pytest.fixture
def anonymous_user() -> AnonymousUser:
    """Provide anonymous user."""
    return AnonymousUser()


@pytest.fixture
def mock_user() -> Mock:
    """Provide user mock."""
    return Mock(spec=Person)


@pytest.fixture
def mock_auth_user(mock_user: Mock) -> Mock:
    """Provide authenticated user mock."""
    mock_user.is_authenticated = True
    return mock_user
