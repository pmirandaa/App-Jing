from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render

from django.views import View
from django.urls import reverse
from django.utils import timezone
from django.core import serializers

from Person.models import Person
from Person.models import PersonAvatar
from Person.models import PersonTemporaryCode

from News.views import HomeNews

import datetime
import random
import json


class RegisterView(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        error = None

        try:
            new_user = User.objects.create_user(
                username=username,
                password=password,
            )

            login(request, new_user)

            return HttpResponseRedirect(reverse('news:home'))

        except:
            error = "Un usuario con ese nombre ya existe."

            return HomeNews.get_with_error(request, error=error)


class LoginView(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)

        return HttpResponseRedirect(reverse('news:home'))


class LogoutView(View):

    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse('news:home'))


class HomePerson(View):

    def get(self, request):
        person = None
        avatar = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)

                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(person=person).latest()

        return render(request, 'Inicio/baseInicio.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "avatar": avatar
                      })


class UnvalidatedPerson(View):

    def get(self, request):
        query = request.GET.get('query')

        persons = Person.objects.filter(
            user__isnull=True,
            name__icontains=query
        ).order_by('name')[:10]

        person_names = []

        for person in persons:
            person_names.append(person.name)

        return HttpResponse(json.dumps(person_names), 'application/json')


class GetQRAndCode(View):

    def random_with_N_digits(self, n):
        range_start = 10**(n-1)
        range_end = (10**n)-1

        return random.randint(range_start, range_end)

    def post(self, request):
        name = request.POST.get('item')

        person = Person.objects.filter(name__iexact=name).first()

        code = self.random_with_N_digits(6)

        PersonTemporaryCode.objects.create(
            person=person,
            code=code,
            expiration_date=timezone.now() + datetime.timedelta(minutes=15)
        )

        return HttpResponse(json.dumps({
            "id": person.id,
            "code": code
        }), 'application/json')


class ValidateUser(View):

    def get(self, request, person_id):

        if request.user.is_authenticated:
            person = Person.objects.get(pk=person_id)
            person.user = request.user

            person.save()

        return HttpResponseRedirect(reverse('news:home'))

    def post(self, request):

        code = request.POST.get('code')
        next = request.POST.get('next')
        if PersonTemporaryCode.objects.filter(
            code=int(code),
            expiration_date__gt=timezone.now()
        ).exists():
            person = PersonTemporaryCode.objects.filter(
                code=int(code),
                expiration_date__gt=timezone.now()
            ).first().person

            person.user = request.user
            person.save()

        return HttpResponseRedirect(next)
