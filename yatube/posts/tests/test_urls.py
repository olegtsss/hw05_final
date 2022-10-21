from django.contrib.auth import get_user
from django.test import override_settings

from posts.tests.test_case import TEMP_MEDIA_ROOT, BaseCaseForTests


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class URLTests(BaseCaseForTests):
    UNEXISTING_PAGE = '/unexisting_page/'

    def test_status_codes(self):
        """Проверка кодов возврата."""
        status_codes = [
            [self.MAIN_PAGE_URL, self.guest, 200],
            [self.GROUP_POSTS_URL, self.guest, 200],
            [self.PROFILE_URL, self.guest, 200],
            [self.POST_DETAIL_URL, self.guest, 200],
            [self.POST_EDIT_URL, self.author, 200],
            [self.POST_EDIT_URL, self.another, 302],
            [self.POST_EDIT_URL, self.guest, 302],
            [self.POST_CREATE_URL, self.author, 200],
            [self.POST_CREATE_URL, self.guest, 302],
            [self.UNEXISTING_PAGE, self.guest, 404],
            [self.FOLLOW_MAIN_PAGE_URL, self.guest, 302],
            [self.FOLLOW_MAIN_PAGE_URL, self.author, 200],
            [self.FOLLOW_URL, self.guest, 302],
            [self.FOLLOW_URL, self.author, 302],
            [self.FOLLOW_URL, self.third, 302],
            [self.UNFOLLOW_URL, self.guest, 302],
            [self.UNFOLLOW_URL, self.author, 404],
            [self.UNFOLLOW_URL, self.third, 302]
        ]
        for url, client, expected_status in status_codes:
            with self.subTest(url=url, user=get_user(client)):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_templates(self):
        """Проверка корректности шаблонов."""
        templates_bank = [
            [self.MAIN_PAGE_URL, self.guest, 'posts/index.html'],
            [self.GROUP_POSTS_URL, self.guest, 'posts/group_list.html'],
            [self.PROFILE_URL, self.guest, 'posts/profile.html'],
            [self.POST_DETAIL_URL, self.guest, 'posts/post_detail.html'],
            [self.POST_EDIT_URL, self.author, 'posts/create_post.html'],
            [self.POST_CREATE_URL, self.author, 'posts/create_post.html'],
            [self.UNEXISTING_PAGE, self.author, 'core/404.html'],
            [self.FOLLOW_MAIN_PAGE_URL, self.author, 'posts/follow.html'],
        ]
        for url, client, expected_template in templates_bank:
            with self.subTest(address=url):
                self.assertTemplateUsed(client.get(url), expected_template)

    def test_redirects(self):
        """Проверка редиректов."""
        self.REDIRECTS_BANK = [
            [self.POST_EDIT_URL, self.another, self.POST_DETAIL_URL],
            [self.POST_EDIT_URL, self.guest, self.POST_EDIT_URL_REDIRECT],
            [self.POST_CREATE_URL, self.guest, self.POST_CREATE_URL_REDIRECT],
            [self.FOLLOW_MAIN_PAGE_URL, self.guest,
                self.FOLLOW_MAIN_PAGE_URL_REDIRECT],
            [self.FOLLOW_URL, self.guest, self.FOLLOW_URL_REDIRECT],
            [self.FOLLOW_URL, self.author, self.PROFILE_URL],
            [self.FOLLOW_URL, self.third, self.PROFILE_URL],
            [self.UNFOLLOW_URL, self.guest, self.UNFOLLOW_URL_REDIRECT],
            [self.UNFOLLOW_URL, self.third, self.PROFILE_URL]
        ]
        for url, client, expected in self.REDIRECTS_BANK:
            with self.subTest(url=url, client=client, expected=expected):
                self.assertRedirects(
                    client.get(url, follow=True), expected
                )
