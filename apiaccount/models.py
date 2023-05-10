"""
В модуле созданные модели базы данных.
"""

from django.contrib.auth.models import User
from django.db import models


class Friend(models.Model):
    """
    Модель списка друзей.

    """

    class Meta:
        verbose_name = 'друг'
        verbose_name_plural = 'друзья'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends', verbose_name='аккаунт')
    friend_name = models.CharField(max_length=255, null=False, verbose_name='имя друга')
    friend_id = models.IntegerField(default=0, verbose_name='ID друга')

    def __str__(self):
        return f'Друзья пользователя - {self.pk}'


class IncomingRequest(models.Model):
    """
    Модель входящей заявки в друзья.

    """

    class Meta:
        verbose_name = 'входящий запрос'
        verbose_name_plural = 'входящие запросы'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming', verbose_name='аккаунт')
    friend_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='имя друга')
    friend_id = models.IntegerField(default=0, null=False, verbose_name='ID друга')


class SentRequest(models.Model):
    """
    Модель оправленной заявки в друзья

    """

    class Meta:
        verbose_name = 'Отправленный запрос'
        verbose_name_plural = 'отправленные запросы'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent', verbose_name='аккаунт')
    friend_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='имя друга')
    friend_id = models.IntegerField(default=0, null=False, verbose_name='ID друга')
