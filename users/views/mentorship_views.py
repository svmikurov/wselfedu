"""Mentorship  views module."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from contrib.mixins_views import CheckLoginPermissionMixin
from users.models import Mentorship, MentorshipRequest, UserModel


def redirect_to_account(request):
    url = reverse_lazy('users:detail', kwargs={'pk': request.user.id})
    return redirect(url)


class InputMentorView(CheckLoginPermissionMixin, TemplateView):
    """Add mentor view."""

    template_name = 'users/send_mentorship_request.html'


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
                request,
                'Пользователь не может стать своим наставником.'
            )
            return redirect_to_account(request)
    except UserModel.DoesNotExist:
        messages.warning(
            request,
            f'Пользователь с именем {mentor_name} не зарегистрирован.',
        )
        return redirect_to_account(request)

    _, created = MentorshipRequest.objects.get_or_create(
        from_user=from_user,
        to_user=to_user,
    )

    if created:
        messages.success(
            request,
            f'Заявка на добавление ментора отправлена {mentor_name}.'
        )
    else:
        messages.warning(
            request,
            f'Заявка на добавление ментора уже была отправлена {mentor_name}.',
        )

    return redirect_to_account(request)


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

    return redirect_to_account(request)


@require_POST
@login_required
def delete_mentorship_request_from_student(
    request: HttpRequest,
    request_pk: int,
) -> HttpResponse:
    """"""
    mentorship_request = MentorshipRequest.objects.get(pk=request_pk)
    if request.user == mentorship_request.student:
        mentorship_request.delete()
        messages.success(request, 'Запрос удален')
    else:
        messages.success(request, 'Вы не можете удалить запрос')
    return redirect_to_account(request)


@require_POST
@login_required
def delete_mentorship_request_to_mentor(
    request: HttpRequest,
    request_pk: int,
) -> HttpResponse:
    """"""
    mentorship_request = MentorshipRequest.objects.get(pk=request_pk)
    if request.user == mentorship_request.from_user:
        mentorship_request.delete()
        messages.success(request, 'Запрос удален')
    else:
        messages.success(request, 'Вы не можете удалить запрос')
    return redirect_to_account(request)


@require_POST
@login_required
def delete_mentorship_mentor(
    request: HttpRequest,
    mentorship_pk: int,
) -> HttpResponse:
    """"""
    mentorship = Mentorship.objects.get(pk=mentorship_pk)
    if request.user == mentorship.student:
        mentorship.delete()
        messages.info(request, 'Наставничество удалено')
    else:
        messages.warning(request, 'Вы не можете удалить наставничество')
    return redirect_to_account(request)


@require_POST
@login_required
def delete_mentorship_student(
    request: HttpRequest,
    mentorship_pk: int,
) -> HttpResponse:
    """"""
    mentorship = Mentorship.objects.get(pk=mentorship_pk)
    if request.user == mentorship.mentor:
        mentorship.delete()
        messages.info(request, 'Наставничество удалено')
    else:
        messages.warning(request, 'Вы не можете удалить наставничество')
    return redirect_to_account(request)
