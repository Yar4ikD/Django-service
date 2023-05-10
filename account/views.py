"""
В модуле прописанные представления для моделей базы данных и взаимодействия с ними.
"""

from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView

from account.forms import SendRequestForm
from account.models import UserProfile, Friend, SentRequest, IncomingRequest


class AllRegisterPeopleView(ListView):
    """
    Класс представления списка всех зарегистрированных пользователей сервиса.
    """

    model = UserProfile
    context_object_name = 'accounts'
    template_name = 'account/all-register-people.html'


class UserDetailView(DetailView):
    """
    Класс представления детальной информации профиля пользователя.

    """

    model = UserProfile
    context_object_name = 'profile'
    template_name = 'account/user-profile-detail.html'


class ListFriendsView(ListView):
    """
    Класс представления списка друзей пользователя.

    """

    template_name = 'account/list-friends.html'
    context_object_name = 'friends'

    def get_queryset(self):
        response = Friend.objects.select_related('owner').filter(owner=self.request.user.profile)

        return response


class ListSendRequestsView(ListView):
    """
    Класс представления списка отправленных заявок в друзья, от пользователя к другому пользователю.

    """

    template_name = 'account/list-send-requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        response = SentRequest.objects.select_related('owner').filter(owner=self.request.user.profile)

        return response


class ListIncomingRequestsView(ListView):
    """
    Класс представления списка входящих запросов на добавления в друзья.

    """

    template_name = 'account/list-incoming-requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        response = IncomingRequest.objects.select_related('owner').filter(owner=self.request.user.profile)
        return response


class DeleteFriendView(DeleteView):
    """
    Класс представления для удаления записей из таблицы - списка друзей (Friend)
    """
    queryset = Friend.objects.select_related('owner')
    template_name = 'account/friend-delete.html'
    context_object_name = 'friend'
    success_url = reverse_lazy('account:list-friends')

    def form_valid(self, form):
        """
        Переопределяем метод класса для добавления логики при удалении пользователя.
        При удалении пользователем друга из своего списка друзей,
        удаляется данный пользователь из списка друзей друга.

        :param form: Данные формы ввода
        :return: HttpResponseRedirect
        """
        success_url = self.get_success_url()
        friend = UserProfile.objects.get(pk=self.object.friend_id)

        Friend.objects.filter(
            owner=friend,
            friend_name=self.request.user.username, friend_id=self.request.user.profile.pk
        ).delete()

        self.object.delete()
        return HttpResponseRedirect(success_url)


class AcceptRequestView(DeleteView):
    """
    Класс представления подтверждения заявки в друзья.
    """

    queryset = IncomingRequest.objects.select_related('owner')
    template_name = 'account/accept-request.html'
    context_object_name = 'friend_request'
    success_url = reverse_lazy('account:list-friends')

    def form_valid(self, form):
        """
        Переопределяем метод класса для добавления логики при подтверждении заявки в друзья.
        При подтверждении пользователи добавляются друг к другу в друзья.
        Заявка в кабинете пользователя удаляется.
        Заявка в кабинете отправителя, также удаляется


        ::param form: Данные формы ввода
        :return: HttpResponseRedirect
        """

        success_url = self.get_success_url()
        friend = UserProfile.objects.get(pk=self.object.friend_id)

        Friend.objects.bulk_create([
            Friend(
                owner=self.request.user.profile,
                friend_name=self.object.friend_name, friend_id=self.object.friend_id
            ),
            Friend(
                owner=friend,
                friend_name=self.request.user.username, friend_id=self.request.user.profile.pk
            )
        ])
        SentRequest.objects.filter(
            owner=self.object.friend_id,
            friend_id=self.request.user.profile.pk,
            friend_name=self.request.user.username
        ).delete()

        self.object.delete()
        return HttpResponseRedirect(success_url)


class DeleteIncomingRequestView(DeleteView):
    """
    Класс представления для удаления входящих заявок в друзья.

    """
    queryset = IncomingRequest.objects.select_related('owner')
    template_name = 'account/delete-incoming-request.html'
    context_object_name = 'friend_request'
    success_url = reverse_lazy('account:list-friends')

    def form_valid(self, form):
        """
        При удалении входящей заявки, удаляется исходная заявка в кабинете пользователя отправителя.

        """
        success_url = self.get_success_url()

        SentRequest.objects.filter(
            owner=self.object.friend_id,
            friend_id=self.request.user.profile.pk,
            friend_name=self.request.user.username
        ).delete()

        self.object.delete()
        return HttpResponseRedirect(success_url)


class CreateOutRequestView(CreateView):
    """
    Клас представления создания запросов в друзья.

    """

    form_class = SendRequestForm
    template_name = 'account/send-request.html'
    success_url = reverse_lazy('account:list-send-request')

    def form_valid(self, form):
        """
        В методе класса добавляем логику работы.
        Если пользователь указал неверные данные или повторно отправляет заявку повторно,
        возвращаем информацию о некорректности данных ввода.
        Если пользователь отправляет заявку в друзья пользователю от которого получил заявку,
        тогда пользователи становятся друзьями, исходные заявки удаляются.

        """

        friend_name = form.cleaned_data['friend_name']
        friend_id = form.cleaned_data['friend_id']
        friend = UserProfile.objects.get(user__username=friend_name, id=friend_id)

        if SentRequest.objects.filter(owner=self.request.user.profile, friend_id=friend_id).exists():
            return redirect('account:all-people')

        if SentRequest.objects.filter(owner=friend, friend_id=self.request.user.profile.pk).exists():

            SentRequest.objects.filter(owner=friend, friend_id=self.request.user.profile.pk).delete()
            IncomingRequest.objects.filter(owner=self.request.user.profile, friend_id=friend_id).delete()

            Friend.objects.bulk_create([
                Friend(owner=self.request.user.profile, friend_name=friend_name, friend_id=friend_id),
                Friend(owner=friend, friend_name=self.request.user.username, friend_id=self.request.user.profile.pk)
            ])
            return redirect('account:list-friends')

        IncomingRequest.objects.create(
            owner=friend,
            friend_name=self.request.user.username,
            friend_id=self.request.user.profile.pk
        )
        form.instance.owner = self.request.user.profile

        return super().form_valid(form)


def get_status_with_another_user(request: HttpRequest, pk) -> HttpResponse:
    """
    Функция представления, возвращает информацию о статусе дружбы пользователей.

    :param request: Get - запрос.
    :param pk: Первичный ключ пользователя.
    :return: HttpResponse
    """

    context = {
        'status': 'Нет нечего'
    }

    if SentRequest.objects.values('owner', 'friend_id').filter(owner=request.user.profile, friend_id=pk).exists():
        context['status'] = 'Отправлена заявка в друзья'

    if IncomingRequest.objects.values('owner', 'friend_id').filter(owner=request.user.profile, friend_id=pk).exists():
        context['status'] = 'Есть входящая заявка'

    if Friend.objects.values('owner', 'friend_id').filter(owner=request.user.profile, friend_id=pk).exists():
        context['status'] = 'Уже друзья'

    return render(request, 'account/get-friend-status.html', context=context)
