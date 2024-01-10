from django.views.generic import DetailView, TemplateView

from contrib_app.mixins import AccountOwnershipMixin
from users.models import UserModel


class UserDetailView(
    AccountOwnershipMixin,
    DetailView,
):
    model = UserModel
    extra_context = {
        'title': 'Личный кабинет',
    }
