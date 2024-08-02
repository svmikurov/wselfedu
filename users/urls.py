from django.urls import path

from users import views

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
    #
    # --======= Mentorship =======--
    # Request to mentor name input page form.
    path(
        'send-mentorship-request/',
        views.InputMentorView.as_view(),
        name='send_mentorship_request',
    ),
    # Request from mentor name input page form.
    path(
        'send-mentorship-request/<int:user_pk>/',
        views.send_mentorship_request,
        name='send_mentorship_request',
    ),
    path(
        'accept-mentorship-request/<int:request_pk>/',
        views.accept_mentorship_request,
        name='accept_mentorship_request',
    ),
    path(
        'delete-mentorship-request-from-student/<int:request_pk>/',
        views.delete_mentorship_request_from_student,
        name='delete_mentorship_request_from_student',
    ),
    path(
        'delete-mentorship-request-to-mentor/<int:request_pk>/',
        views.delete_mentorship_request_to_mentor,
        name='delete_mentorship_request_to_mentor',
    ),

    path(
        'delete-mentorship-mentor/<int:mentorship_pk>/',
        views.delete_mentorship_mentor,
        name='delete_mentorship_mentor',
    ),
    path(
        'delete-mentorship-student/<int:mentorship_pk>/',
        views.delete_mentorship_student,
        name='delete_mentorship_student',
    ),
    # -- EndMentorship --
]
