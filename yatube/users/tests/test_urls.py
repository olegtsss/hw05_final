from django.test import Client, TestCase, override_settings

from posts.models import User
from posts.tests.test_case import TEMP_MEDIA_ROOT


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')

    def setUp(self):
        self.guest = Client()
        self.author = Client()
        self.author.force_login(URLTests.user)

    def test_public_url(self):
        """Проверка доступности public URLs."""
        templates_url_names = {
            '/auth/logout/': 'users/logged_out.html',
            '/auth/login/': 'users/login.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/reset/NA/64i-1e05c466b8bdb9b9a860/':
                'users/password_reset_confirm.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest.get(address)
                self.assertTemplateUsed(response, template)

    def test_private_url(self):
        """Проверка доступности private URLs."""
        templates_url_names = {
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/password_change/': 'users/password_change_form.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.author.get(address)
                self.assertTemplateUsed(response, template)

    def test_private_url_for_guest(self):
        """Проверка редиректа для гостевого входа."""
        templates_url_names = {
            '/auth/password_change/done/':
                '/auth/login/?next=/auth/password_change/done/',
            '/auth/password_change/':
                '/auth/login/?next=/auth/password_change/',
        }
        for address, redirect_url in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest.get(address, follow=True)
                self.assertRedirects(response, redirect_url)

    def test_private_url_for_guest_template(self):
        """Проверка, какой шаблон будет отображен
        при редиректе для гостевого входа.
        """
        templates_url_names = {
            '/auth/password_change/done/': 'users/login.html',
            '/auth/password_change/': 'users/login.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest.get(address, follow=True)
                self.assertTemplateUsed(response, template)
