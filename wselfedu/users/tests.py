from django.template.response import TemplateResponse
from django.test import Client, TestCase
from django.urls import reverse_lazy
from faker import Faker

from contrib_app.contrib_test import flash_message_test
from wselfedu.users.models import UserModel


class RegistrationUserViewTest(TestCase):
    """ Тест регистрации пользователя """

    def setUp(self):
        """
        Создаем пустую тестовую базу данных.
        Объявляем url, redirect_url регистрации пользователя.
        Объявляем сообщение об успешной регистрации пользователя.
        Создаем данные пользователя.
        """
        self.client: Client = Client()
        self.url: str = reverse_lazy('user:create')
        self.redirect_url: str = reverse_lazy('home')
        self.success_message: str = 'Вы успешно зарегистрировались'

        self.faker: Faker = Faker()
        self.fake_username: str = self.faker.user_name()
        self.fake_password: str = self.faker.password()
        self.user_data: dict = {
            'username': self.fake_username,
            'password1': self.fake_password,
            'password2': self.fake_password,
        }

    def test_get(self):
        """ Тест страницы регистрации пользователя """
        response: TemplateResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """ Тест результата регистрации пользователя """
        response: TemplateResponse = self.client.post(self.url, self.user_data)

        self.assertRedirects(response, self.redirect_url, 302)
        self.assertTrue(UserModel.objects.filter(
            username=self.fake_username
        ).exists())
        flash_message_test(response, self.success_message)
