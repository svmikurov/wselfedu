from django.template.response import TemplateResponse
from django.test import Client, TestCase
from django.urls import reverse_lazy
from faker import Faker
from faker.generator import Generator

from wselfedu.users.models import UserModel


class UserDetailTest(TestCase):
    """ Тест личного кабинета пользователя """

    def setUp(self):
        """
        Создаем тестовую базу данных.
        Создаем тестового пользователя.
        Объявляем url личного кабинета пользователя.
        Создаем данные пользователя.
        """
        self.client: Client = Client()
        self.faker: Generator = Faker()

        # Создаем тестового пользователя
        # 'Generator' object has no attribute 'username'
        fake_username: str = self.faker.user_name()
        self.fake_user = UserModel.objects.create(username=fake_username)

        # Создаем url-адрес личного кабинета тестового пользователя
        self.url = reverse_lazy(
            'user:detail',
            kwargs={'pk': self.fake_user.pk}
        )

    def test_get(self):
        """ Тест статуса личного кабинета """
        response: TemplateResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
