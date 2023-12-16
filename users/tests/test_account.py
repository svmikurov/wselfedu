from django.template.response import TemplateResponse
from django.test import Client, TestCase
from django.urls import reverse_lazy
from faker import Faker
from faker.generator import Generator

from contrib_app.contrib_test import flash_message_test
from users.models import UserModel


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
        faker: Generator = Faker()

        # Создаем тестового пользователя
        # 'Generator' object has no attribute 'username'
        fake_username: str = faker.user_name()
        self.fake_user = UserModel.objects.create(username=fake_username)
        self.fake_name_not_owner = faker.user_name()
        self.fake_user_not_owner = UserModel.objects.create(username=self.fake_name_not_owner)

        # Создаем url-адрес личного кабинета тестового пользователя
        self.url = reverse_lazy(
            'users:detail',
            kwargs={'pk': self.fake_user.pk}
        )
        self.redirect_no_permission = reverse_lazy('home')
        self.message_no_permission = 'Так не получится!'

    def test_get(self):
        """ Тест статуса личного кабинета """
        self.client.force_login(self.fake_user)
        response: TemplateResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_not_owner(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_no_permission, 302)
        flash_message_test(response, self.message_no_permission)

        self.client.force_login(self.fake_user_not_owner)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_no_permission, 302)
        flash_message_test(response, self.message_no_permission)
