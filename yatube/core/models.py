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
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[0:LENGTH_TEXT]
