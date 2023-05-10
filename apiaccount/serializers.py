from django.contrib.auth.models import User
from rest_framework import serializers

from apiaccount.models import Friend, IncomingRequest, SentRequest


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User.

    """
    class Meta:
        model = User
        fields = ['username', 'pk']


class FriendSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Friend.

    """

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Friend
        fields = '__all__'


class IncomingRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели IncomingRequest.

    """

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = IncomingRequest
        fields = '__all__'


class SentRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели SentRequest.

    """

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SentRequest
        fields = '__all__'
