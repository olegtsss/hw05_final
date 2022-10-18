from django import forms
from django.test import override_settings

from posts.models import Post
from posts.tests.test_case import TEMP_MEDIA_ROOT, BaseCaseForTests


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(BaseCaseForTests):
    def test_create_post_in_database(self):
        """Cоздаётся новая запись в базе данных c корректными атрибутами."""
        before_posts = set(Post.objects.all())
        form_data = {
            'text': 'Второй пост.',
            'group': self.group.id,
            'image': self.GIF_ANOTHER_FILE
        }
        response = self.author.post(
            self.POST_CREATE_URL, form_data, follow=True
        )
        after_posts = set(Post.objects.all())
        added_posts_set = after_posts - before_posts
        self.assertEqual(len(added_posts_set), 1)
        self.assertRedirects(response, self.PROFILE_URL)
        post = added_posts_set.pop()
        self.assertTrue(post.author, self.user)
        self.assertTrue(post.group.id, form_data['group'])
        self.assertTrue(post.text, form_data['text'])
        self.assertTrue(post.image, form_data['image'])

    def test_edit_post(self):
        """После редактирования происходит изменение поста."""
        form_data = {
            'text': 'Третий пост.' * 2,
            'group': self.group_another.id
        }
        response = self.author.post(
            self.POST_EDIT_URL, data=form_data, follow=True
        )
        post = response.context['post']
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.author, self.post.author)
        self.assertRedirects(response, self.POST_DETAIL_URL)

    def test_post_create_and_edit_context(self):
        """Проверка контекста для контроллера post_create и post_edit."""
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for url in [self.POST_CREATE_URL, self.POST_EDIT_URL]:
            response = self.author.get(url)
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, expected)
