from django.urls import path, include

from apiaccount.views import (
    AllRegisterPeopleApiView,
    FriendApiView,
    IncomingRequestApiView,
    SentRequestApiView,
    DeleteFriendApiView,
    DeleteIncomingRequestApiView,
    AcceptRequestApiView,
    GetStatusApiView,
)

app_name = 'apiaccount'

urlpatterns = [

    path('register/', include('djoser.urls')),

    path('all-people/', AllRegisterPeopleApiView.as_view(), name='all-people'),

    path('friends/', FriendApiView.as_view(), name='friends'),
    path('friend/<int:pk>/delete/', DeleteFriendApiView.as_view(), name='delete-friend'),

    path('incoming-requests/', IncomingRequestApiView.as_view(), name='incoming-requests'),
    path('incoming-requests/<int:pk>/accept/', AcceptRequestApiView.as_view(), name='incoming-requests-accept'),
    path('incoming-requests/<int:pk>/delete/', DeleteIncomingRequestApiView.as_view(), name='incoming-requests-delete'),

    path('sent-request/', SentRequestApiView.as_view(), name='sent-request'),

    path('get-status/<int:friend_pk>/', GetStatusApiView.as_view(), name='get-status')

    # re_path(r'^auth/', include('djoser.urls.authtoken')),

]
