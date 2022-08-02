from time import sleep
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django.views import View
from django.urls import reverse
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from University.models import UniversityEvent

from Person.models import Person
from Person.models import PersonAvatar
from Person.models import PersonTemporaryCode
from Person.serializers import PersonSerializer

from Match.models import Match

from Sport.models import Sport

from University.models import University

from News.views import HomeNews

import datetime
import random
import json

from utils import is_valid_param, bool_param

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def dispatch(self, request, *args, **kwargs):
        sleep(0.5)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        event = self.request.query_params.get('event')
        last_name = self.request.query_params.get('last_name')
        first_name = self.request.query_params.get('first_name')
        university = self.request.query_params.get('university')
        sport = self.request.query_params.get('sport')
        is_admin = bool_param(self.request.query_params.get('is_admin'))
        is_coord_sport = bool_param(self.request.query_params.get('is_coord_sport'))
        is_coord_uni = bool_param(self.request.query_params.get('is_coord_uni'))
        if is_valid_param(event):
            queryset = queryset.filter(event=event)
        if is_valid_param(last_name):
            queryset = queryset.filter(last_name__icontains=last_name)
        if is_valid_param(first_name):
            queryset = queryset.filter(name__icontains=first_name)
        if is_valid_param(university):
            queryset = queryset.filter(university=university)
        if is_valid_param(sport):
            queryset = queryset.filter(playerteam__team__sport=sport)
        if is_valid_param(is_admin):
            queryset = queryset.filter(is_admin=is_admin)
        if is_valid_param(is_coord_sport):
            queryset = queryset.filter(sport__isnull=False).distinct()
        if is_valid_param(is_coord_uni):
            queryset = queryset.filter(is_university_coordinator=is_coord_uni)
        queryset = queryset.order_by('last_name')
        return queryset
    
    @method_decorator(cache_page(60))
    @action(detail=False)
    def filters(self, request):
        data = {}
        event = self.request.query_params.get('event')
        if is_valid_param(event):
            university = University.objects.filter(
                universityevent__event__exact=event).values('pk', 'short_name')
            data["university"] = [
                {"value": x["pk"], "label": x["short_name"]} for x in university]
            sports = Sport.objects.all().values('pk', 'name')
            data["sport"] = [{"value": x["pk"], "label": x["name"]}
                             for x in sports]
        return Response(data)
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

        university_host = UniversityEvent.objects.filter(
            is_host=True, event__year=datetime.datetime.now().year).first()

        matches = Match.objects.all()

        sports = Sport.objects.all()

        universities = University.objects.all().order_by('-overall_score')
        important_scores = len(University.objects.filter(overall_score__gt=0)) != 0

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)
                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(
                        person=person).latest()

        return render(request, 'Inicio/baseInicio.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "avatar": avatar,
                          "university": university_host.university,
                          "matches": matches,
                          "sports": sports,
                          "universities": universities,
                          "important_scores": important_scores,
                      })


class UnvalidatedPerson(View):

    def get(self, request):
        query_name = request.GET.get('query').split(' ')[0]

        try:
            query_surname = request.GET.get('query').split(' ')[1]
        except:
            query_surname = '' 

        persons = Person.objects.filter(
            user__isnull=True,
            name__icontains=query_name,
            last_name__icontains=query_surname,
        ).order_by('name')[:10]

        person_names = []

        for person in persons:
            person_names.append(f'{person.name} {person.last_name}')

        return HttpResponse(json.dumps(person_names), 'application/json')


class PersonsList(View):

    def get(self, request):
        query_name = request.GET.get('query').split(' ')[0]

        try:
            query_surname = request.GET.get('query').split(' ')[1]
        except:
            query_surname = '' 

        persons = Person.objects.filter(
            name__icontains=query_name,
            last_name__icontains=query_surname,
        ).order_by('name')[:10]


        person_names = []

        for person in persons:
            person_names.append(f'{person.name} {person.last_name}')

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

            success = "Su cuenta se ha validado exitosamente"

            return HomeNews.get_with_success(request, success=success)
        else:
            error = "Debe iniciar sesión con su perfil antes de intentar validar su cuenta."

            return HomeNews.get_with_error(request, error=error)

    def post(self, request):

        code = request.POST.get('code')
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

            success = "Su cuenta se ha validado exitosamente"

            return HomeNews.get_with_success(request, success=success)
        else:
            error = "No se ha podido validar, recuerde que su numero de validación es valido solo por 15 minutos"

            return HomeNews.get_with_error(request, error=error)
