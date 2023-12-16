from django.test import Client, TestCase
from django.urls import reverse_lazy
from faker import Faker
from faker.generator import Generator

from contrib_app.contrib_test import flash_message_test
from users.models import UserModel


class UserUpdateTest(TestCase):
    """ Тест редактирования данных пользователя """

    def setUp(self):
        """
        Создаем базу данных.
        Создаем пользователя.
        Создаем новое имя для пользователя.
        Создаем url личного кабинета пользователя.
        """
        self.client: Client = Client()
        faker: Generator = Faker()

        self.fake_username: str = faker.user_name()
        fake_password: str = faker.password(length=10)
        self.fake_user = UserModel.objects.create(
            username=self.fake_username,
            password=fake_password,
        )
        self.fake_updated_username: str = faker.user_name()
        self.fake_updated_data = {
            'username': self.fake_updated_username,
            'password1': fake_password,
            'password2': fake_password,
        }
        self.fake_name_not_owner = faker.user_name()
        self.fake_user_not_owner = UserModel.objects.create(
            username=self.fake_name_not_owner
        )
        self.url = reverse_lazy(
            'users:update',
            kwargs={'pk': self.fake_user.pk}
        )
        # self.redirect_url = reverse_lazy(
        #     'users:detail',
        #     kwargs={'pk': self.fake_user.pk}
        # )
        self.success_message = 'Вы обновили свои данные'
        self.redirect_no_permission = reverse_lazy('home')
        self.message_no_permission = 'Так не получится!'

    def test_get(self):
        """ Тестируем статус страницы обновления данных """
        self.client.force_login(self.fake_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_not_owner(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_no_permission, 302)
        flash_message_test(response, self.message_no_permission)

        self.client.force_login(self.fake_user_not_owner)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_no_permission, 302)
        flash_message_test(response, self.message_no_permission)

    def test_post(self):
        self.client.force_login(self.fake_user)
        response = self.client.post(self.url, self.fake_updated_data)

        # self.assertRedirects(response, self.redirect_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserModel.objects.filter(
            username=self.fake_updated_username
        ).exists())
        flash_message_test(response, self.success_message)

    def test_post_not_owner(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, self.redirect_no_permission, 302)
        self.assertTrue(UserModel.objects.filter(
            username=self.fake_username
        ).exists())
        flash_message_test(response, self.message_no_permission)

        self.client.force_login(self.fake_user_not_owner)
        response = self.client.post(self.url)
        self.assertRedirects(response, self.redirect_no_permission, 302)
        self.assertTrue(UserModel.objects.filter(
            username=self.fake_username
        ).exists())
        flash_message_test(response, self.message_no_permission)
