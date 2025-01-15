from django.test import Client, TestCase, override_settings

from posts.tests.test_case import TEMP_MEDIA_ROOT


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class StaticPagesURLTests(TestCase):
    static_urls = {
        '/about/author/': 'about/author.html',
        '/about/tech/': 'about/tech.html'
    }

    def setUp(self):
        self.guest = Client()

    def test_static_urls_exists_at_desired_location(self):
        """Проверка доступности статических адресов."""
        for url in self.static_urls:
            with self.subTest(field=url):
                response = self.guest.get(url)
                self.assertEqual(response.status_code, 200)

    def test_static_urls_uses_correct_templates(self):
        """Проверка шаблонов для статических адресов."""
        for url, template in self.static_urls.items():
            with self.subTest(field=url):
                response = self.guest.get(url)
                self.assertTemplateUsed(response, template)
