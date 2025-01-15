from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
LENGTH_TEXT = 15


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет разные атрибуты."""
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField(
        'Текст',
        help_text='Введите текст поста'
    )
    author = models.ForeignKey(
        User,
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        text = self.text[0:LENGTH_TEXT]
        author = self.author.username
        pub_date = self.pub_date.strftime('%Y:%m:%d')
        return f'{text}, {author}, {pub_date}'
