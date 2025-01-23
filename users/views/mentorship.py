"""Mentorship views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, TemplateView

from contrib.views.general import (
    CheckObjectOwnershipMixin,
    DeleteWithProfileRedirectView,
)
from contrib.views.mentorship import CheckMentorshipMixin
from users.models import Mentorship, MentorshipRequest, UserApp


def redirect_to_mentorship_profile(user_id: int) -> HttpResponseRedirect:
    """Redirect to profile page."""
    url = reverse_lazy('users:mentorship_profile', kwargs={'pk': user_id})
    return redirect(url)


class MentorshipView(CheckObjectOwnershipMixin, DetailView):
    """Mentorship profile view."""

    model = UserApp
    template_name = 'users/mentorship/mentorship.html'

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add data to context."""
        mentorship_request_mentors = (
            MentorshipRequest.objects.filter(from_user=self.request.user)
            .annotate(
                request_pk=F('pk'),
                mentor_name=F('to_user__username'),
            )
            .values('request_pk', 'mentor_name')
        )

        mentorship_request_students = (
            MentorshipRequest.objects.filter(to_user=self.request.user)
            .annotate(
                request_pk=F('pk'),
                student_name=F('from_user__username'),
            )
            .values('request_pk', 'student_name')
        )

        mentorship_students = (
            Mentorship.objects.filter(
                mentor=self.request.user,
            )
            .annotate(
                student_pk=F('student__pk'),
                student_name=F('student__username'),
            )
            .values('id', 'student_pk', 'student_name')
        )

        mentorship_mentors = (
            Mentorship.objects.filter(
                student=self.request.user,
            )
            .annotate(mentor_name=F('mentor__username'))
            .values('id', 'mentor_name')
        )

        context = super().get_context_data()
        context['mentorship_request_mentors'] = mentorship_request_mentors
        context['mentorship_request_students'] = mentorship_request_students
        context['mentorship_students'] = mentorship_students
        context['mentorship_mentors'] = mentorship_mentors
        return context


@require_POST
@login_required
def send_mentorship_request(
    request: HttpRequest,
    **kwargs: object,
) -> HttpResponse:
    """Send request to create a mentorship, the view."""
    from_user = request.user
    mentor_name = request.POST['input_mentor_name']

    try:
        to_user = UserApp.objects.get(username=mentor_name)
    except UserApp.DoesNotExist:
        msg = f'Пользователь с именем {mentor_name} не зарегистрирован'
        messages.warning(request, msg)
        return redirect_to_mentorship_profile(from_user.id)
    else:
        has_mentor = Mentorship.objects.filter(
            mentor=to_user, student=request.user
        ).exists()

        if from_user == to_user:
            msg = 'Пользователь не может стать своим наставником'
        elif has_mentor:
            msg = 'Запрашиваемый пользователь уже ваш наставник'
        else:
            _, created = MentorshipRequest.objects.get_or_create(
                from_user=from_user, to_user=to_user
            )
            if created:
                msg = f'Заявка отправлена {mentor_name}'
            else:
                msg = f'Заявка уже была отправлена {mentor_name}'

        messages.warning(request, msg)
        return redirect_to_mentorship_profile(from_user.id)


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

    return redirect_to_mentorship_profile(request.user.id)


class DeleteMentorshipRequestView(DeleteWithProfileRedirectView):
    """Delete mentorship request, the view."""

    model = MentorshipRequest
    success_message = 'Запрос удален'

    def test_func(self) -> bool:
        """Check mentor permission."""
        [mentorship_users] = self.model.objects.filter(
            pk=self.get_object().pk
        ).values_list('to_user', 'from_user')
        return self.request.user.pk in mentorship_users


class DeleteMentorshipView(DeleteWithProfileRedirectView):
    """Delete mentorship view."""

    model = Mentorship
    success_message = 'Наставничество удалено'

    def test_func(self) -> bool:
        """Check mentor permission."""
        [mentorship_users] = self.model.objects.filter(
            pk=self.get_object().pk
        ).values_list('student', 'mentor')
        return self.request.user.pk in mentorship_users


class AssignItemToStudentView(CheckMentorshipMixin, TemplateView):
    """Assign item to study to a student by a mentor, the view."""

    template_name = 'users/mentorship/assign_to_student.html'
