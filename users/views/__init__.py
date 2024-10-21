"""Package of views of the Users application."""

# ruff: noqa: I001
from users.views.auth import (
    UserLoginView,
    UserLogoutView,
)
from users.views.user import (
    CreateUserView,
    DeleteUserView,
    UpdateUserView,
    UsersListView,
)
from users.views.mentorship import (
    InputMentorView,
    accept_mentorship_request,
    send_mentorship_request,
    AddExerciseDataView,
    AddWordByMentorToStudentViewRedirect,
    DeleteMentorshipRequestView,
    DeleteMentorshipView,
    MentorshipView,
)
from users.views.profile import UserDetailView

__all__ = (
    'UserLoginView',
    'UserLogoutView',
    'CreateUserView',
    'UpdateUserView',
    'DeleteUserView',
    'UsersListView',
    'UserDetailView',
    'MentorshipView',
    'InputMentorView',
    'accept_mentorship_request',
    'send_mentorship_request',
    'DeleteMentorshipRequestView',
    'DeleteMentorshipView',
    'AddExerciseDataView',
    'AddWordByMentorToStudentViewRedirect',
)
