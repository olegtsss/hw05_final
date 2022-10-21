from django.conf import settings
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse

from posts.models import Follow, Post
from posts.tests.test_case import TEMP_MEDIA_ROOT, BaseCaseForTests


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(BaseCaseForTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.POST_URL = reverse(
            'posts:post_detail', args=[cls.post.id]
        )
        Follow.objects.create(user=cls.user_another, author=cls.user)

    def test_contexts(self):
        """Проверка контекстов приложения posts"""
        case = [
            self.MAIN_PAGE_URL,
            self.GROUP_POSTS_URL,
            self.PROFILE_URL,
            self.POST_URL,
            self.FOLLOW_MAIN_PAGE_URL
        ]
        for url in case:
            with self.subTest(address=url):
                if url != self.POST_URL:
                    posts = self.another.get(url).context['page_obj']
                    self.assertEqual(len(posts), 1)
                    post = posts[0]
                else:
                    post = self.guest.get(url).context['post']
                self.assertEqual(self.post.author, post.author)
                self.assertEqual(self.post.group, post.group)
                self.assertEqual(self.post.text, post.text)
                self.assertEqual(self.post.id, post.id)
                self.assertEqual(self.post.image, post.image)

    def test_other_context_profile(self):
        """Дополнительная проверка контекста в приложении posts для profile"""
        response = self.guest.get(self.PROFILE_URL)
        self.assertEqual(response.context['author'], self.user)

    def test_other_context_group(self):
        """Дополнительная проверка контекста в приложении posts для group"""
        group = self.guest.get(self.GROUP_POSTS_URL).context['group']
        self.assertEqual(group.id, self.group.id)
        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.slug, self.group.slug)
        self.assertEqual(group.description, self.group.description)

    def test_paginators(self):
        """Проверка пагинаторов приложения posts"""
        cases = [
            [self.MAIN_PAGE_URL, settings.COUNT_OBJECTS_IN_PAGE],
            [f'{self.MAIN_PAGE_URL}?page=2', 1],
            [self.GROUP_POSTS_URL, settings.COUNT_OBJECTS_IN_PAGE],
            [f'{self.GROUP_POSTS_URL}?page=2', 1],
            [self.PROFILE_URL, settings.COUNT_OBJECTS_IN_PAGE],
            [f'{self.PROFILE_URL}?page=2', 1],
            [self.PROFILE_URL, settings.COUNT_OBJECTS_IN_PAGE],
            [f'{self.PROFILE_URL}?page=2', 1],
            [self.FOLLOW_MAIN_PAGE_URL, settings.COUNT_OBJECTS_IN_PAGE],
            [f'{self.FOLLOW_MAIN_PAGE_URL}?page=2', 1]
        ]
        Post.objects.bulk_create(
            Post(
                text=f'Тест пост {n}.',
                author=self.user,
                group=self.group
            )
            for n in range(settings.COUNT_OBJECTS_IN_PAGE)
        )
        for url, expected in cases:
            with self.subTest(address=url):
                response = self.another.get(url)
                self.assertEqual(len(response.context['page_obj']), expected)

    def test_index_page_cashe(self):
        """Проверка работы кэша для списка постов"""
        page = self.guest.get(self.MAIN_PAGE_URL).content
        Post.objects.all().delete()
        self.assertEqual(
            page, self.guest.get(self.MAIN_PAGE_URL).content
        )
        cache.clear()
        self.assertNotEqual(
            page, self.guest.get(self.MAIN_PAGE_URL).content
        )

    def test_user_can_follow_to_another_authors(self):
        """
        Авторизованный пользователь может подписываться на других пользователей
        """
        self.third.get(self.FOLLOW_URL)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user_third, author=self.user)
        )

    def test_user_can_unfollow_to_another_authors(self):
        """
        Авторизованный пользователь может отписываться от других пользователей
        """
        self.another.get(self.UNFOLLOW_URL)
        self.assertFalse(
            Follow.objects.filter(
                user=self.user_another, author=self.user)
        )

    def test_another_group_without_test_post(self):
        """Проверка, что пост не попал в чужие групп-ленты"""
        case = [
            self.ANOTHER_GROUP_POSTS_URL,
            self.FOLLOW_MAIN_PAGE_URL
        ]
        for url in case:
            with self.subTest(address=url):
                posts = self.third.get(url).context['page_obj']
                self.assertIsNot(self.post, posts)
