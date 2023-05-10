from django.urls import path

from account.views import (

    ListFriendsView,
    AllRegisterPeopleView,
    UserDetailView,
    CreateOutRequestView,
    ListSendRequestsView,
    ListIncomingRequestsView,
    DeleteFriendView,
    AcceptRequestView,
    get_status_with_another_user,
    DeleteIncomingRequestView,
)

app_name = 'account'

urlpatterns = [

    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('all-people/', AllRegisterPeopleView.as_view(), name='all-people'),
    path('profile-details/<int:pk>/', UserDetailView.as_view(), name='profile-detail'),
    path('delete/<int:pk>/friend/', DeleteFriendView.as_view(), name='delete-friend'),

    path('send-request/', CreateOutRequestView.as_view(), name='send-request'),
    path('list-send-requests/', ListSendRequestsView.as_view(), name='list-send-request'),

    path('list-incoming-requests/', ListIncomingRequestsView.as_view(), name='list-incoming-request'),
    path('delete-incoming-request/<int:pk>/', DeleteIncomingRequestView.as_view(), name='delete-incoming-request'),
    path('accept-request/<int:pk>/', AcceptRequestView.as_view(), name='accept-request'),

    path('get-status/<int:pk>/', get_status_with_another_user, name='get-status'),

]
