from django.test import Client, TestCase
from django.urls import reverse_lazy
from faker import Faker
from faker.generator import Generator

from contrib_app.contrib_test import flash_message_test
from wselfedu.users.models import UserModel


class UserDeleteTest(TestCase):
    """ Тест удаления пользователя """

    def setUp(self):

        self.client: Client = Client()
        faker: Generator = Faker()

        self.fake_username = faker.user_name()
        self.fake_user = UserModel.objects.create(username=self.fake_username)
        self.fake_name_not_owner = faker.user_name()
        self.fake_user_not_owner = UserModel.objects.create(username=self.fake_name_not_owner)

        self.url = reverse_lazy(
            'user:delete',
            kwargs={'pk': self.fake_user.pk}
        )
        self.redirect_url = reverse_lazy('home')
        self.redirect_no_permission = reverse_lazy('home')
        self.success_message = 'Пользователь удален'
        self.message_no_permission = 'У вас нет разрешения на эти действия'

    def test_get(self):
        self.client.force_login(self.fake_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserModel.objects.filter(
            username=self.fake_username
        ).exists())

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
        self.client.force_login(self.fake_user)
        response = self.client.post(self.url)

        self.assertRedirects(response, self.redirect_url, 302)
        self.assertFalse(UserModel.objects.filter(
            username=self.fake_username
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
