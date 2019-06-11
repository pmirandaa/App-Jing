from django.http.response import HttpResponseRedirect

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect

from django.views import View
from django.urls import reverse


class RegisterView(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        new_user = User.objects.create_user(
            username=username,
            password=password,
        )

        login(request, new_user)

        return HttpResponseRedirect(reverse('news:non-auth-news'))


class LoginView(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)

        return HttpResponseRedirect(reverse('news:non-auth-news'))


class LogoutView(View):

    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse('news:non-auth-news'))
