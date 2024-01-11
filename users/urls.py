from django.urls import path

from users import views

app_name = 'users'
urlpatterns = [
    # <!--======== Users list ========-->
    path(
        'list/',
        views.UsersListView.as_view(),
        name='list',
    ),
    # <!-- End Users list -->
    # <!--======== Auth users =======-->
    path(
        'registration/',
        views.UserRegistrationView.as_view(template_name='form.html'),
        name='create',
    ),
    path(
        'login/',
        views.UserLoginView.as_view(template_name='users/login.html'),
        name='login',
    ),
    path(
        'logout/',
        views.UserLogoutView.as_view(),
        name='logout',
    ),  # <!-- End Auth users -->
    # <!--======== Users account editions =======-->
    path(
        '<pk>/account/',
        views.UserDetailView.as_view(template_name='users/account.html'),
        name='detail',
    ),
    path(
        '<pk>/update/',
        views.UserUpdateView.as_view(template_name='form.html'),
        name='update',
    ),
    path(
        '<pk>/delete/',
        views.UserDeleteView.as_view(template_name='delete.html'),
        name='delete',
    ),
    # <!-- End Users account editions -->
]
