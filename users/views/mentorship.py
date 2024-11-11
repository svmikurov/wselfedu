"""Mentorship views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBase,
    HttpResponseRedirect,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (
    DetailView,
    RedirectView,
    TemplateView,
)

from contrib.views.general import (
    CheckLoginPermissionMixin,
    CheckObjectOwnershipMixin,
    DeleteWithProfileRedirectView,
)
from users.models import Mentorship, MentorshipRequest, UserApp


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


class AddWordByMentorToStudentViewRedirect(RedirectView):
    """Redirect with added data in session view."""

    url = reverse_lazy('foreign:mentor_adds_words_for_student_study')
    """Url to redirect.
    """

    def get(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponseBase:
        """Add student id to session."""
        request.session['student'] = kwargs.get('student')
        response = super().get(request, *args, **kwargs)
        return response


def redirect_to_mentorship_profile(
    request: HttpRequest,
) -> HttpResponseRedirect:
    """Redirect to profile page."""
    url = reverse_lazy(
        'users:mentorship_profile', kwargs={'pk': request.user.id}
    )
    return redirect(url)


class InputMentorView(CheckLoginPermissionMixin, TemplateView):
    """Add mentor view."""

    template_name = 'users/mentorship/send_mentorship_request.html'


class AddExerciseDataView(TemplateView):
    """Add data for student study view."""

    template_name = 'users/mentorship/add_data.html'

    def get(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponse:
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
        to_user = UserApp.objects.get(username=mentor_name)
        if from_user == to_user:
            messages.warning(
                request, 'Пользователь не может стать своим наставником'
            )
            return redirect_to_mentorship_profile(request)

        to_user_is_mentor = Mentorship.objects.filter(
            mentor=to_user, student=request.user
        ).exists()
        if to_user_is_mentor:
            messages.warning(
                request, 'Запрашиваемый пользователь уже ваш наставник'
            )
            return redirect_to_mentorship_profile(request)

    except UserApp.DoesNotExist:
        messages.warning(
            request,
            f'Пользователь с именем {mentor_name} не зарегистрирован',
        )
        return redirect_to_mentorship_profile(request)

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

    return redirect_to_mentorship_profile(request)


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

    return redirect_to_mentorship_profile(request)


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
