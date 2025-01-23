"""User app urls module."""

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
]

mentorship_urls = [
    path(
        # Mentorship profile
        'mentorship/<int:pk>/',
        views.MentorshipView.as_view(),
        name='mentorship_profile',
    ),
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
        'delete-mentorship-request/<int:pk>/',
        views.DeleteMentorshipRequestView.as_view(),
        name='delete_mentorship_request',
    ),
    path(
        'delete-mentorship/<int:pk>/',
        views.DeleteMentorshipView.as_view(),
        name='delete_mentorship',
    ),
    # --======= Mentor management =======--
    path(
        'add-exercise/<int:student_id>/',
        views.AddExerciseDataView.as_view(),
        name='add_exercise',
    ),
]

urlpatterns += mentorship_urls
