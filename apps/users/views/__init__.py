"""Contains Uses app views."""

__all__ = [
    'AcceptMentorshipRequest',
    'AssignExerciseView',
    'AssignedExercisesView',
    'DeleteMentorRequestView',
    'DeleteMentorView',
    'DeleteStudentRequestView',
    'DeleteStudentView',
    'MentorshipView',
    'ProfileView',
    'SignUpView',
]

from .assignation import (
    AssignedExercisesView,
    AssignExerciseView,
)
from .mentorship import (
    AcceptMentorshipRequest,
    DeleteMentorRequestView,
    DeleteMentorView,
    DeleteStudentRequestView,
    DeleteStudentView,
    MentorshipView,
)
from .profile import ProfileView
from .user import SignUpView
