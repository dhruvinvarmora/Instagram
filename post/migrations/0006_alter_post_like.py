# Generated by Django 4.2.3 on 2023-08-01 06:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0005_alter_post_options_post_like_delete_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, default=None, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
