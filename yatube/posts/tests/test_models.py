from core.models import LENGTH_TEXT
from django.test import override_settings

from posts.models import Follow, Post
from posts.tests.test_case import TEMP_MEDIA_ROOT, BaseCaseForTests


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostModelTest(BaseCaseForTests):
    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.assertEqual(self.group.title, str(self.group))
        for model in [self.post, self.comment]:
            text = model.text[0:LENGTH_TEXT]
            author = model.author.username
            pub_date = model.pub_date.strftime('%Y:%m:%d')
            self.assertEqual(f'{[text, author, pub_date]}', str(model))
        follow = Follow.objects.create(
            user=self.user, author=self.user_another
        )
        self.assertEqual(str(follow), f'{[self.user, self.user_another]}')

    def test_models_have_correct_verboses(self):
        """Проверяем, что у моделей корректно работают verbose_name."""
        field_verbose_name = {
            'text': 'Текст',
            'pub_date': 'Дата создания',
            'author': 'Автор',
            'group': 'Группа',
        }
        field_help_text = {
            'text': 'Введите текст поста',
            'pub_date': '',
            'author': '',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_value in field_verbose_name.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Post._meta.get_field(field).verbose_name,
                    expected_value
                )
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Post._meta.get_field(field).help_text,
                    expected_value
                )
