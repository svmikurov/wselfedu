from users.views.auth_views import (
    UserLoginView,
    UserLogoutView,
)
from users.views.crud_user_views import (
    CreateUserView,
    UpdateUserView,
    DeleteUserView,
    UsersListView,
    UserDetailView,
)

__all__ = [
    'UserLoginView',
    'UserLogoutView',
    'CreateUserView',
    'UpdateUserView',
    'DeleteUserView',
    'UsersListView',
    'UserDetailView',
]
