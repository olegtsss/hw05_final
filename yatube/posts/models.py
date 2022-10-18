from core.models import CreatedModel

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
LENGTH_TEXT = 15


class Group(models.Model):
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('Уникальный идентификатор', unique=True)
    description = models.TextField('Описание',)

    class Meta:
        verbose_name = "группу"
        verbose_name_plural = "Группы на портале"

    def __str__(self):
        return self.title


class Post(CreatedModel):
    text = models.TextField(
        'Текст',
        help_text='Введите текст поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "пост"
        verbose_name_plural = "Посты на портале"

    def __str__(self):
        return self.text[0:LENGTH_TEXT]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        'Комментарий',
        max_length=400,
        help_text='Введите комментарий'
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии постов"

    def __str__(self):
        return self.text[0:LENGTH_TEXT]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан'
    )

    class Meta:
        verbose_name = "подписку"
        verbose_name_plural = "Подписки на портале"
