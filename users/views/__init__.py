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
    accept_mentorship_request,
    send_mentorship_request,
    AssignItemToStudentView,
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
    'accept_mentorship_request',
    'send_mentorship_request',
    'DeleteMentorshipRequestView',
    'DeleteMentorshipView',
    'AssignItemToStudentView',
    'AddWordByMentorToStudentViewRedirect',
)
