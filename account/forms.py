"""
В модуле прописана форма для отправки заявки в друзья
"""

from django import forms
from django.core.exceptions import ValidationError

from account.models import SentRequest
from authuser.models import UserProfile


class SendRequestForm(forms.ModelForm):
    """
    Форма для отправки заявки пользователю на добавления в друзья.

    """

    class Meta:
        model = SentRequest
        fields = ['friend_name', 'friend_id', ]

    def clean_friend_id(self):
        """
        Метод проверят поля для ввода id профиля пользователя.
        ID > 0

        :return: friend_id
        """

        friend_id = self.cleaned_data['friend_id']
        if friend_id < 1:
            raise ValidationError('ID должно быть больше 0')

        return friend_id

    def clean(self):
        """
        Проверяем существует ли пользователь.

        :return: ValidationError or None
        """

        cleaned_data = super().clean()
        friend_name = cleaned_data.get("friend_name")
        friend_id = cleaned_data.get("friend_id")

        friend = UserProfile.objects.filter(user__username=friend_name, id=friend_id).exists()
        if not friend:
            raise ValidationError('Пользователя с такими данными не существует')
