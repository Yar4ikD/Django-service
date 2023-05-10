from django.urls import path

from authuser.views import UserRegisterView, UserLoginView, UserLogoutView, AboutMeView

app_name = 'authuser'

urlpatterns = [
    path('about-me/', AboutMeView.as_view(), name='about-me'),

    path('register/', UserRegisterView.as_view(), name='register-user'),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),

]
