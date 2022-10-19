from django import forms
from django.test import override_settings

from posts.models import Comment, Post
from posts.tests.test_case import TEMP_MEDIA_ROOT, BaseCaseForTests


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(BaseCaseForTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form_data = {
            'text': 'Второй пост.',
            'group': cls.group.id,
            'image': cls.GIF_ANOTHER_FILE
        }
        cls.edited_form_data = {
            'text': 'Третий пост.' * 2,
            'group': cls.group_another.id,
            # 'image': cls.GIF_ANOTHER_FILE
        }

    def test_create_post_in_database(self):
        """Cоздаётся новая запись в базе данных c корректными атрибутами."""
        before_posts = set(Post.objects.all())
        response = self.author.post(
            self.POST_CREATE_URL, self.form_data, follow=True
        )
        after_posts = set(Post.objects.all())
        added_posts_set = after_posts - before_posts
        self.assertEqual(len(added_posts_set), 1)
        self.assertRedirects(response, self.PROFILE_URL)
        post = added_posts_set.pop()
        self.assertTrue(post.author, self.user)
        self.assertTrue(post.group.id, self.form_data['group'])
        self.assertTrue(post.text, self.form_data['text'])
        self.assertTrue(post.image, self.form_data['image'])

    def test_guest_cannot_create_post(self):
        """Гость не может создать пост."""
        before_posts = set(Post.objects.all())
        self.guest.post(
            self.POST_CREATE_URL, self.form_data, follow=True
        )
        after_posts = set(Post.objects.all())
        self.assertEqual(after_posts, before_posts)

    def test_edit_post(self):
        """После редактирования происходит изменение поста."""
        response = self.author.post(
            self.POST_EDIT_URL, data=self.edited_form_data, follow=True
        )
        post = response.context['post']
        self.assertEqual(post.text, self.edited_form_data['text'])
        self.assertEqual(post.group.id, self.edited_form_data['group'])
        # self.assertEqual(
        #    post.image.name, f"posts/{self.edited_form_data['image']}"
        # )
        self.assertEqual(post.author, self.post.author)
        self.assertRedirects(response, self.POST_DETAIL_URL)

    def test_not_author_cannot_edit_post(self):
        """Не автор и гость не могут отредактировать пост."""
        self.another.post(self.POST_EDIT_URL, data=self.edited_form_data)
        self.guest.post(self.POST_EDIT_URL, data=self.edited_form_data)
        post = self.author.post(self.POST_DETAIL_URL).context['post']
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.group.id, self.post.group.id)
        self.assertEqual(post.image.name, self.post.image)
        self.assertEqual(post.author, self.post.author)

    def test_post_create_and_edit_context(self):
        """Проверка контекста для контроллера post_create и post_edit."""
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField
        }
        for url in [self.POST_CREATE_URL, self.POST_EDIT_URL]:
            response = self.author.get(url)
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_auth_user_can_comment_post(self):
        """
        Проверка, что авторизованный пользователь может комментировать пост
        """
        before_comments = set(Comment.objects.all())
        new_text_comment = {'text': 'Тестовый комментарий'}
        self.another.post(self.POST_COMMENT, data=new_text_comment)
        after_comments = set(Comment.objects.all())
        added_comments_set = after_comments - before_comments
        self.assertEqual(len(added_comments_set), 1)
        comment = added_comments_set.pop()
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user_another)
        self.assertEqual(comment.text, new_text_comment['text'])

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
        self.assertEqual(after_comments, before_comments)
