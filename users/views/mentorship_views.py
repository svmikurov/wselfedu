"""Mentorship  views module."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (
    RedirectView,
    TemplateView,
)

from contrib.mixins_views import (
    CheckLoginPermissionMixin,
    DeleteWithProfileRedirectView,
)
from users.models import Mentorship, MentorshipRequest, UserModel


class AddWordByMentorToStudentViewRedirect(RedirectView):
    """Redirect with added data in session view."""

    url = reverse_lazy('english:mentor_adds_words_for_student_study')
    """Url to redirect.
    """

    def get(self, request, *args, **kwargs):
        """Add student id to session."""
        request.session['student'] = kwargs.get('student')
        response = super().get(request, *args, **kwargs)
        return response


def redirect_to_profile(request):
    """Redirect to profile page."""
    url = reverse_lazy('users:detail', kwargs={'pk': request.user.id})
    return redirect(url)


class InputMentorView(CheckLoginPermissionMixin, TemplateView):
    """Add mentor view."""

    template_name = 'users/mentor/send_mentorship_request.html'


class AddExerciseDataView(TemplateView):
    """Add data for student study view."""

    template_name = 'users/mentor/add_data.html'

    def get(self, request, *args, **kwargs):
        """Add student id to session."""
        request.session['student_id'] = kwargs['student_id']
        response = super().get(request, *args, **kwargs)
        return response


@require_POST
@login_required
def send_mentorship_request(
    request: HttpRequest,
    **kwargs: object,
) -> HttpResponse:
    """Send request to create a mentorship view."""
    from_user = request.user
    mentor_name = request.POST['input_mentor_name']

    try:
        to_user = UserModel.objects.get(username=mentor_name)
        if from_user == to_user:
            messages.warning(
                request, 'Пользователь не может стать своим наставником'
            )
            return redirect_to_profile(request)
    except UserModel.DoesNotExist:
        messages.warning(
            request,
            f'Пользователь с именем {mentor_name} не зарегистрирован',
        )
        return redirect_to_profile(request)

    _, created = MentorshipRequest.objects.get_or_create(
        from_user=from_user,
        to_user=to_user,
    )

    if created:
        messages.success(
            request, f'Заявка на добавление ментора отправлена {mentor_name}'
        )
    else:
        messages.warning(
            request,
            f'Заявка на добавление ментора уже была отправлена {mentor_name}',
        )

    return redirect_to_profile(request)


@require_POST
@login_required
def accept_mentorship_request(
    request: HttpRequest,
    request_pk: int,
) -> HttpResponse:
    """Accept mentorship view."""
    mentorship_request = MentorshipRequest.objects.get(pk=request_pk)

    if mentorship_request.to_user == request.user:
        mentorship = Mentorship.objects.create(
            mentor=mentorship_request.to_user,
            student=mentorship_request.from_user,
        )
        mentorship_request.delete()
        messages.success(request, f'Вы стали наставником {mentorship.student}')
    else:
        messages.warning(request, 'Вы не можете стать наставником')

    return redirect_to_profile(request)


class DeleteMentorshipRequestView(DeleteWithProfileRedirectView):
    """Delete mentorship request by mentor view."""

    model = MentorshipRequest
    success_message = 'Запрос удален'

    def check_permission(self) -> bool:
        """Check mentor permission."""
        [mentorship_users] = MentorshipRequest.objects.filter(
            pk=self.get_object().pk
        ).values_list('to_user', 'from_user')
        return self.request.user.pk in mentorship_users


class DeleteMentorshipView(DeleteWithProfileRedirectView):
    """Delete mentorship by student view."""

    model = Mentorship
    success_message = 'Наставничество удалено'

    def check_permission(self) -> bool:
        """Check mentor permission."""
        [mentorship_users] = Mentorship.objects.filter(
            pk=self.get_object().pk
        ).values_list('student', 'mentor')
        return self.request.user.pk in mentorship_users
