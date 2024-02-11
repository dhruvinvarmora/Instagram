# Generated by Django 4.2.3 on 2023-07-27 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_follow', models.BooleanField(default=True)),
                ('followed_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_followed', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]