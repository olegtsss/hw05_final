from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import User
from posts.tests.test_case import TEMP_MEDIA_ROOT


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class SignFormTests(TestCase):
    @classmethod
    def setUp(cls):
        cls.guest_client = Client()

    def test_signup(self):
        """При заполнении формы signup создаётся новый пользователь."""
        posts_count = User.objects.count()
        form_data = {
            'first_name': 'TestName',
            'last_name': 'TestLastName',
            'username': 'testuser',
            'email': 'test@test.test',
            'password1': 'PaSSwOrdPaSSwOrd',
            'password2': 'PaSSwOrdPaSSwOrd',
        }
        self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertEqual(User.objects.count(), posts_count + 1)
