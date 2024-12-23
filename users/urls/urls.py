"""User app urls module."""

from django.urls import path

from users import views
from users.urls.mentor_urls import mentor_urls

app_name = 'users'

urlpatterns = [
    # <!--======== Auth users =======-->
    path(
        'login/',
        views.UserLoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        views.UserLogoutView.as_view(),
        name='logout',
    ),  # <!-- End Auth users -->
    # <!--======== CRUD Users =======-->
    path(
        'registration/',
        views.CreateUserView.as_view(),
        name='create',
    ),
    path(
        '<int:pk>/update/',
        views.UpdateUserView.as_view(),
        name='update',
    ),
    path(
        '<int:pk>/delete/',
        views.DeleteUserView.as_view(),
        name='delete',
    ),
    path(
        'list/',
        views.UsersListView.as_view(),
        name='list',
    ),
    path(
        '<int:pk>/account/',
        views.UserDetailView.as_view(),
        name='detail',
    ),
    # <!-- End CRUD Users -->
]

urlpatterns.extend(
    mentor_urls,
)
