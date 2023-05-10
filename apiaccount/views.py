"""
В модуле прописанные API-представления для моделей базы данных и взаимодействия с ними.

"""

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apiaccount.models import Friend, IncomingRequest, SentRequest
from apiaccount.serializers import (
    UserProfileSerializer,
    FriendSerializer,
    IncomingRequestSerializer,
    SentRequestSerializer
)


class AllRegisterPeopleApiView(generics.ListAPIView):
    """
    API Представления просмотра зарегистрированных пользователей.

    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class FriendApiView(generics.ListAPIView):
    """
    API Представления списка друзей.
    """
    serializer_class = FriendSerializer

    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(owner=user)


class DeleteFriendApiView(generics.DestroyAPIView):
    """
    API Представления удаления пользователя из друзей.

    """

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def perform_destroy(self, instance):
        """
        При удалении - пользователи взаимоудаляются из друзей, друг у друга.

        """

        friend = User.objects.get(pk=instance.friend_id)
        Friend.objects.filter(
            owner=friend,
            friend_name=self.request.user.username, friend_id=self.request.user.pk
        ).delete()

        instance.delete()


class IncomingRequestApiView(generics.ListAPIView):
    """
    API Представления просмотра списка входящих заявок в друзья.

    """
    serializer_class = IncomingRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return IncomingRequest.objects.filter(owner=user)


class AcceptRequestApiView(APIView):
    """
    API Представления подтверждения входящей заявки в друзья.

    """

    def post(self, request: Request, pk) -> Response:
        try:
            inc_req = IncomingRequest.objects.get(owner=self.request.user, pk=pk)

        except ObjectDoesNotExist:
            return Response({"error": "Заявки не существует!"}, status=status.HTTP_400_BAD_REQUEST)

        friend = User.objects.get(pk=inc_req.friend_id)

        Friend.objects.bulk_create([
            Friend(owner=self.request.user, friend_name=friend.username, friend_id=friend.pk),
            Friend(owner=friend, friend_name=self.request.user.username, friend_id=self.request.user.pk)
        ])

        SentRequest.objects.filter(
            owner=friend,
            friend_id=self.request.user.pk,
            friend_name=self.request.user.username
        ).delete()

        inc_req.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteIncomingRequestApiView(generics.DestroyAPIView):
    """
    API Представления удаления входящей заявки.

    """

    queryset = IncomingRequest.objects.all()
    serializer_class = IncomingRequestSerializer

    def perform_destroy(self, instance):
        """
        При удаление входной заявки, исходная заявка отправителя удаляется.

        """

        friend = User.objects.get(pk=instance.friend_id)

        SentRequest.objects.filter(
            owner=friend,
            friend_name=self.request.user.username,
            friend_id=self.request.user.pk
        ).delete()

        instance.delete()


class SentRequestApiView(generics.ListCreateAPIView):
    """
    API Представления просмотра и создания запросов в друзья.

    """

    serializer_class = SentRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return SentRequest.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        """
        В методе класса добавляем логику работы API.
        Если пользователь указал неверные данные или повторно отправляет заявку повторно,
        возвращаем информацию о некорректности данных ввода.
        Если пользователь отправляет заявку в друзья пользователю от которого получил заявку,
        тогда пользователи становятся друзьями, исходные заявки удаляются.

        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        friend_name = self.request.data['friend_name']
        friend_id = self.request.data['friend_id']

        if not User.objects.filter(username=friend_name, pk=friend_id).exists():
            return Response({"error": "Пользователь с такими данными не зарегистрирован."})

        if SentRequest.objects.filter(owner=self.request.user, friend_name=friend_name, friend_id=friend_id).exists():
            return Response({"Вы уже отправили запрос этому пользователю."})

        if SentRequest.objects.filter(owner=friend_id, friend_id=self.request.user.pk).exists():

            SentRequest.objects.filter(owner=friend_id, friend_id=self.request.user.pk).delete()
            IncomingRequest.objects.filter(owner=self.request.user, friend_id=friend_id).delete()

            owner = User.objects.get(pk=self.request.user.pk)
            friend = User.objects.get(pk=friend_id)

            Friend.objects.bulk_create([
                Friend(owner=owner, friend_name=friend_name, friend_id=friend_id),
                Friend(owner=friend, friend_name=self.request.user.username, friend_id=self.request.user.pk)
                ])

            return Response({f"Вы с {friend_name} уже друзья"}, status=status.HTTP_201_CREATED)

        friend = User.objects.get(pk=friend_id)
        IncomingRequest.objects.create(
            owner=friend,
            friend_name=self.request.user.username,
            friend_id=self.request.user.pk
        )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetStatusApiView(APIView):
    """
    API Представления получения статуса дружбы пользователей.

    """

    def post(self, request: Request, friend_pk: int) -> Response:

        context = {
            "status": "Нет нечего"
        }

        if SentRequest.objects.values('owner', 'friend_id')\
                .filter(owner=request.user, friend_id=friend_pk).exists():
            context['status'] = "Отправлена заявка в друзья"

        if IncomingRequest.objects.values('owner', 'friend_id')\
                .filter(owner=request.user, friend_id=friend_pk).exists():
            context['status'] = "Есть входящая заявка"

        if Friend.objects.values('owner', 'friend_id')\
                .filter(owner=request.user, friend_id=friend_pk).exists():
            context['status'] = "Уже друзья"

        return Response(context, status=status.HTTP_200_OK)
