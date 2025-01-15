from core.models import CreatedModel, User

from django.db import models


class Group(models.Model):
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('Уникальный идентификатор', unique=True)
    description = models.TextField('Описание',)

    class Meta:
        verbose_name = 'группу'
        verbose_name_plural = 'Группы на портале'

    def __str__(self):
        return self.title


class Post(CreatedModel):
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

    class Meta(CreatedModel.Meta):
        verbose_name = 'пост'
        verbose_name_plural = 'Посты на портале'


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый пост'
    )

    class Meta(CreatedModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии на портале'


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
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'подписку'
        verbose_name_plural = 'Подписки на портале'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user is not author',
            ),
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_following')
        ]

    def __str__(self):
        return f'{self.user.username}, {self.author.username}'
