from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from authuser.models import UserProfile


class AboutMeView(TemplateView):
    model = UserProfile
    template_name = 'authuser/about-user.html'
    context_object_name = 'user'


class UserRegisterView(CreateView):
    """
    Представление регистрации пользователя.
    При успешной регистрации, производиться автоматическая авторизация.

    """

    form_class = UserCreationForm
    success_url = reverse_lazy('authuser:about-me')
    template_name = 'authuser/register-user.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        UserProfile.objects.create(user=self.object)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(self.request,
                            username=username,
                            password=password)

        login(request=self.request, user=user)
        return response


class UserLoginView(LoginView):
    """
    Представление для авторизации пользователя.

    """

    template_name = 'authuser/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('authuser:login')
