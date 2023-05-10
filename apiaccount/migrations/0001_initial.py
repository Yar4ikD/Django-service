# Generated by Django 4.2.1 on 2023-05-10 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_name', models.CharField(max_length=255, verbose_name='имя друга')),
                ('friend_id', models.IntegerField(default=0, verbose_name='ID друга')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent', to=settings.AUTH_USER_MODEL, verbose_name='аккаунт')),
            ],
            options={
                'verbose_name': 'Отправленный запрос',
                'verbose_name_plural': 'отправленные запросы',
            },
        ),
        migrations.CreateModel(
            name='IncomingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_name', models.CharField(max_length=255, verbose_name='имя друга')),
                ('friend_id', models.IntegerField(default=0, verbose_name='ID друга')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming', to=settings.AUTH_USER_MODEL, verbose_name='аккаунт')),
            ],
            options={
                'verbose_name': 'входящий запрос',
                'verbose_name_plural': 'входящие запросы',
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_name', models.CharField(max_length=255, verbose_name='имя друга')),
                ('friend_id', models.IntegerField(default=0, verbose_name='ID друга')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL, verbose_name='аккаунт')),
            ],
            options={
                'verbose_name': 'друг',
                'verbose_name_plural': 'друзья',
            },
        ),
    ]