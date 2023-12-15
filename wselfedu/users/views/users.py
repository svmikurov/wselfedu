from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

from wselfedu.users.forms import UserRegistrationForm


class UserRegistrationView(
    CreateView,
):
    form_class = UserRegistrationForm
    extra_context = {
        'title': 'Регистрация',
        'btn_name': 'Зарегистрироваться',
    }
    success_url = reverse_lazy('home')
    success_message = 'Вы успешно зарегистрировались'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
