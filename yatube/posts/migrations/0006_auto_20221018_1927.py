# Generated by Django 2.2.16 on 2022-10-18 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20221018_1910'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='user_cannot_follow_himself',
        ),
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_following',
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user', 'author')},
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='user is not author'),
        ),
    ]
