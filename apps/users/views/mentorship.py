"""Defines mentorship views."""

from typing import Any

from dependency_injector.wiring import Provide, inject
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import FormView

from apps.core.generic.views import HtmxDeleteView
from di import MainContainer

from ..exception import MentorshipError
from ..forms import SendMentorshipRequestForm  # type: ignore
from ..models import CustomUser, Mentorship, MentorshipRequest
from ..presenters.iabc import IMentorshipPresenter
from ..services.iabc import IMentorshipService


class MentorshipView(LoginRequiredMixin, FormView):  # type: ignore[type-arg]
    """Mentorship view."""

    form_class = SendMentorshipRequestForm
    template_name = 'users/mentorship/mentorship.html'

    @inject
    def get_context_data(
        self,
        presenter: IMentorshipPresenter = Provide[
            MainContainer.users_container.mentorship_presenter
        ],
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Add context data."""
        context = super().get_context_data(**kwargs)
        context.update(presenter.get_mentorship_relations(self.user))
        return context

    @inject
    def form_valid(
        self,
        form: forms.Form,
        service: IMentorshipService = Provide[
            MainContainer.users_container.mentorship_service
        ],
    ) -> HttpResponse:
        """Create mentorship request by student."""
        try:
            service.create_mentorship_request(
                student=self.user,
                mentor_username=form.cleaned_data['mentor_username'],
            )
        except MentorshipError as e:
            form.add_error(None, str(e.html_message))
            html = self._get_html(form=form)
        else:
            # TODO: Fix automatic filling of form fields when the page
            #       is forced to reload after submitting the form.
            html = self._get_html(form=SendMentorshipRequestForm())

        return HttpResponse(html)

    def form_invalid(self, form: forms.Form) -> HttpResponse:
        """If the form is invalid, render the invalid form."""
        if 'Hx-Request' in self.request.headers:
            # Render only the partial html for HTMX request
            return HttpResponse(self._get_html(form=form))
        return super().form_invalid(form)

    @property
    def user(self) -> CustomUser:
        """Get user."""
        user = self.request.user
        if not isinstance(user, CustomUser):
            raise PermissionDenied('Invalid user type')
        return user

    @inject
    def _get_html(
        self,
        form: forms.Form,
        presenter: IMentorshipPresenter = Provide[
            MainContainer.users_container.mentorship_presenter
        ],
    ) -> str:
        """Get HTML to render on request HTMX."""
        request_to_mentors = presenter.get_requests_to_mentors(
            self.user,
        )
        return render_to_string(
            'users/mentorship/partials/table_student_requests.html',
            {
                'request_to_mentors': request_to_mentors,
                'form': form,
            },
            request=self.request,
        )


class AcceptMentorshipRequest(LoginRequiredMixin, View):
    """Accept the student request to mentorships."""

    @inject
    def post(
        self,
        request: HttpRequest,
        pk: int,
        *args: object,
        service: IMentorshipService = Provide[
            MainContainer.users_container.mentorship_service
        ],
        **kwargs: object,
    ) -> HttpResponse:
        """Send POST request."""
        service.accept_mentorship_request(request_id=pk, mentor=self.mentor)
        return HttpResponse(self._get_html())

    def _get_html(
        self,
        presenter: IMentorshipPresenter = Provide[
            MainContainer.users_container.mentorship_presenter
        ],
    ) -> str:
        """Get HTML to render on request HTMX."""
        return render_to_string(
            'users/mentorship/partials/tables_mentorships.html',
            {
                'mentor_mentorships': presenter.get_students(
                    self.mentor,
                ),
                'request_from_students': presenter.get_requests_from_students(
                    self.mentor,
                ),
            },
            request=self.request,
        )

    @property
    def mentor(self) -> CustomUser:
        """Get mentor."""
        mentor = self.request.user
        if not isinstance(mentor, CustomUser):
            raise PermissionDenied('Invalid user type')
        return mentor


class DeleteStudentView(HtmxDeleteView):
    """Delete the student from mentorship."""

    model = Mentorship

    def _get_owner(self) -> CustomUser:
        owner: CustomUser = self.get_object().mentor
        return owner


class DeleteMentorView(HtmxDeleteView):
    """Delete the mentor from mentorship."""

    model = Mentorship

    def _get_owner(self) -> CustomUser:
        owner: CustomUser = self.get_object().student
        return owner


class DeleteStudentRequestView(HtmxDeleteView):
    """Delete by mentor the mentorship request from student."""

    model = MentorshipRequest

    def _get_owner(self) -> CustomUser:
        owner: CustomUser = self.get_object().to_user
        return owner


class DeleteMentorRequestView(HtmxDeleteView):
    """Delete by student the mentorship request to mentor."""

    model = MentorshipRequest

    def _get_owner(self) -> CustomUser:
        owner: CustomUser = self.get_object().from_user
        return owner
