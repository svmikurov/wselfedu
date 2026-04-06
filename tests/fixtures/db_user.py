"""User DB fixtures."""

import pytest

from apps.users.models import Mentorship, Person

# -----------------------------------------------
# User
# -----------------------------------------------


@pytest.fixture
def user() -> Person:
    """Provide user."""
    return Person.objects.create_user(username='user', password='pass')


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
