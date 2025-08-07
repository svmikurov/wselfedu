"""Defines mentorship request form."""

from django import forms


class SendMentorshipRequest(forms.Form):
    """Form to send request on mentorship."""

    mentor_name = forms.CharField()
