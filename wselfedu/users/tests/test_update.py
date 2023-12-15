from django.test import Client, TestCase
from django.urls import reverse_lazy
from faker import Faker
from faker.generator import Generator

from contrib_app.contrib_test import flash_message_test
from wselfedu.users.models import UserModel


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

        self.fake_username = faker.user_name()
        self.fake_updated_username = faker.user_name()
        self.fake_user = UserModel.objects.create(username=self.fake_username)
        self.fake_name_not_owner = faker.user_name()
        self.fake_user_not_owner = UserModel.objects.create(username=self.fake_name_not_owner)

        self.url = reverse_lazy(
            'user:edit',
            kwargs={'pk': self.fake_user.pk}
        )
        self.redirect_url = reverse_lazy(
            'user:detail',
            kwargs={'pk': self.fake_user.pk}
        )
        self.success_message = 'Вы успешно обновили свои данные'
        self.redirect_no_permission = reverse_lazy('home')
        self.message_no_permission = 'У вас нет разрешения на эти действия'

    def test_get(self):
        """ Тестируем статус страницы обновления данных """
        self.client.force_login(self.fake_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_not_owner(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_no_permission, 302)
        self.assertTrue(UserModel.objects.filter(
            username=self.fake_username
        ).exists())
        flash_message_test(response, self.message_no_permission)

        self.client.force_login(self.fake_user_not_owner)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_no_permission, 302)
        self.assertTrue(UserModel.objects.filter(
            username=self.fake_username
        ).exists())
        flash_message_test(response, self.message_no_permission)

    def test_post(self):
        """
        Отправляем обновленные данные пользователя.
        Тестируем редирект с новым именем пользователя.
        Тестируем существование пользователя с новым именем.
        Тестируем сообщением об успешном обновлении пользователя.
        """
        self.client.force_login(self.fake_user)
        response = self.client.post(self.url, self.fake_updated_username)

        self.assertRedirects(response, self.url, 302)
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
