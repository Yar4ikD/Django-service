from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Модель профиля пользователя.

    """

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='пользователь')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='время регистрации')

    def __str__(self):
        return f'Аккаунт пользователя {self.pk}'
