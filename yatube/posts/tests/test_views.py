from django.conf import settings
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse

from posts.models import Comment, Follow, Post, User
from posts.tests.test_case import TEMP_MEDIA_ROOT, BaseCaseForTests


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(BaseCaseForTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.POST_URL = reverse(
            'posts:post_detail', args=[cls.post.id]
        )

    def test_contexts(self):
        """Проверка контекстов приложения posts"""
        case = [
            self.MAIN_PAGE_URL,
            self.GROUP_POSTS_URL,
            self.PROFILE_URL,
            self.POST_URL
        ]
        for url in case:
            with self.subTest(address=url):
                if url != self.POST_URL:
                    posts = self.guest.get(url).context['page_obj']
                    self.assertEqual(len(posts.object_list), 1)
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
            [f'{self.PROFILE_URL}?page=2', 1]
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
                response = self.guest.get(url)
                self.assertEqual(len(response.context['page_obj']), expected)

    def test_another_group_without_test_post(self):
        """Проверка, что пост не попал в чужую групп-ленту"""
        posts = self.guest.get(
            self.ANOTHER_GROUP_POSTS_URL
        ).context['page_obj']
        self.assertIsNot(self.post, posts)

    def test_auth_user_can_comment_post(self):
        """
        Проверка, что авторизованный пользователь
        может комментировать пост
        """
        before_comments = set(Comment.objects.all())
        self.another.post(
            self.POST_COMMENT,
            data={'text': 'Тестовый комментарий'}
        )
        after_comments = set(Comment.objects.all())
        added_comments_set = after_comments - before_comments
        self.assertEqual(len(added_comments_set), 1)
        comment = added_comments_set.pop()
        response_comment = self.guest.post(
            self.POST_DETAIL_URL
        ).context['comments'][0]
        self.assertTrue(comment.post, response_comment.post)
        self.assertTrue(comment.author, response_comment.author)
        self.assertTrue(comment.text, response_comment.text)
        self.assertTrue(comment.pub_date, response_comment.pub_date)

    def test_not_auth_user_cannot_comment_post(self):
        """
        Проверка, что не авторизованный пользователь
        не может комментировать пост
        """
        before_comments = set(Comment.objects.all())
        self.guest.post(
            self.POST_COMMENT,
            data={'text': 'Тестовый комментарий'}
        )
        after_comments = set(Comment.objects.all())
        added_comments_set = after_comments - before_comments
        self.assertEqual(len(added_comments_set), 0)

    def test_index_page_cashe(self):
        """Проверка работы кэша для списка постов"""
        posts = self.guest.get(
            self.MAIN_PAGE_URL
        ).context['page_obj'].object_list
        self.assertIn(self.post, posts)
        page = self.guest.get(self.MAIN_PAGE_URL).content
        Post.objects.all().delete()
        self.assertEqual(
            page, self.guest.get(self.MAIN_PAGE_URL).content
        )
        cache.clear()
        self.assertNotEqual(
            page, self.guest.get(self.MAIN_PAGE_URL).content
        )

    def test_user_can_follow_unfollow_to_another_authors(self):
        """
        Авторизованный пользователь может подписываться
        на других пользователей и отписываться от них
        """
        before_follows = set(Follow.objects.all())
        self.another.get(self.FOLLOW_URL)
        after_follows = set(Follow.objects.all())
        added_follows = after_follows - before_follows
        self.assertEqual(len(added_follows), 1)
        follow = added_follows.pop()
        self.assertEqual(follow.user, self.user_another)
        self.assertEqual(follow.author, self.user)
        self.another.get(self.UNFOLLOW_URL)
        after_unfollow = set(Follow.objects.all())
        new_follows = after_unfollow - after_follows
        self.assertEqual(len(new_follows), 0)

    def test_new_post_on_page_follower(self):
        self.another.get(self.FOLLOW_URL)
        self.assertIn(
            self.post,
            self.another.get(
                self.FOLLOW_MAIN_PAGE_URL
            ).context['page_obj'].object_list
        )
        new_post = Post.objects.create(
            text='Второй пост.',
            author=self.user,
            group=self.group
        )
        self.assertIn(
            new_post,
            self.another.get(
                self.FOLLOW_MAIN_PAGE_URL
            ).context['page_obj'].object_list
        )
        self.assertNotIn(
            new_post,
            self.third.get(
                self.FOLLOW_MAIN_PAGE_URL
            ).context['page_obj'].object_list
        )
