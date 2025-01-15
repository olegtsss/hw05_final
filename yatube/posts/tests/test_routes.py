from django.test import TestCase, override_settings
from django.urls import reverse

from posts.tests.test_case import TEMP_MEDIA_ROOT
from posts.urls import app_name

SLUG = 'test-slug'
USERNAME = 'HasNoName'
POST_ID = 0

CASES = [
    ['index', None, '/'],
    ['group_posts', [SLUG], f'/group/{SLUG}/'],
    ['profile', [USERNAME], f'/profile/{USERNAME}/'],
    ['post_edit', [POST_ID], f'/posts/{POST_ID}/edit/'],
    ['post_detail', [POST_ID], f'/posts/{POST_ID}/'],
    ['post_create', None, '/create/'],
    ['profile_follow', [USERNAME], f'/profile/{USERNAME}/follow/'],
    ['profile_unfollow', [USERNAME], f'/profile/{USERNAME}/unfollow/'],
    ['follow_index', None, '/follow/'],
    ['add_comment', [POST_ID], f'/posts/{POST_ID}/comment/']
]


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RoutesTests(TestCase):
    def test_routes(self):
        """Тест, что рассчитываемые маршруты дают ожидаемые явные урлы"""
        for route, args, url in CASES:
            with self.subTest(route=route):
                self.assertEqual(
                    reverse(f'{app_name}:{route}', args=args), url
                )
