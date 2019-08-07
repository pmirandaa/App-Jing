from django.shortcuts import render
from django.views import View

from django.http.response import HttpResponseRedirect
from django.urls import reverse

from Person.models import Person
from Event.models import Event
from University.models import University
from Location.models import Location
from Sport.models import Sport

from django.contrib.auth.models import User


class AdminPanel(View):

    def get(self, request):

        people = Person.objects.all()
        events = Event.objects.all()
        unis = University.objects.all()
        locations = Location.objects.all()
        sports = Sport.objects.all()
        sport_types = Sport.SPORT_TYPE
        genders = Sport.SPORT_GENDER
        sport_coords = Person.objects.filter(is_sports_coordinator=True)
        unis_coords = Person.objects.filter(is_university_coordinator=True)

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)

                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(
                        person=person).latest()

        return render(request, 'Administration/baseAdmin.html',
                      {
                          "name": request.user.username,
                          "people": people,
                          "events": events,
                          "universities": unis,
                          "locations": locations,
                          "person": person,
                          "sports": sports,
                          "sport_types": sport_types,
                          "genders": genders,
                          "sports_coords": sport_coords,
                          "unis_coords": unis_coords
                      })


class AdminCreateUser(View):

    def post(self, request):

        rut = request.POST.get('rut').strip()
        nombres = request.POST.get('nombres').strip()
        email = request.POST.get('email').strip()
        apellidos = request.POST.get('apellidos').strip()
        is_admin = request.POST.get('is_admin', False) == 'on'
        is_organizer = request.POST.get('is_organizer', False) == 'on'
        is_university_coordinator = request.POST.get(
            'is_uni_coordinator', False) == 'on'
        is_sports_coordinator = request.POST.get(
            'is_sports_coordinator', False) == 'on'
        event_id = request.POST.get('event')
        university_id = request.POST.get('university')
        phone = request.POST.get('phone').strip()

        event = Event.objects.get(id=event_id)
        university = University.objects.get(id=university_id)

        user = User(
            username=rut,
            email=email,
            first_name=nombres,
            last_name=apellidos
        )
        user.save()

        person = Person(
            user=user,
            event=event,
            name='{}, {}'.format(apellidos, nombres),
            email=email,
            university=university,
            rut=rut,
            phone_number=phone,
            is_admin=is_admin,
            is_organizer=is_organizer,
            is_university_coordinator=is_university_coordinator,
            is_sports_coordinator=is_sports_coordinator
        )

        try:
            person.save()
        except:
            user.delete()

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminDeleteUser(View):
    def post(self, request):

        user_id = request.POST.get('user')

        user = User.objects.get(id=user_id)

        if user:
            user.delete()

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminCreateUniversity(View):
    def post(self, request):
        name = request.POST.get('name')
        city = request.POST.get('city')
        short_name = request.POST.get('short-name')

        university = University(
            name=name, city=city, short_name=short_name
        )

        university.save()

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminDeleteUniversity(View):
    def post(self, request):

        uni_id = request.POST.get('university')

        university = University.objects.get(id=uni_id)

        if university:
            university.delete()

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminCreateLocation(View):
    def post(self, request):
        name = request.POST.get('name')
        address = request.POST.get('address')
        uni_id = request.POST.get('university')

        university = University.objects.get(id=uni_id)

        location = Location(
            name=name, address=address, university=university
        )

        location.save()

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminDeleteLocation(View):
    def post(self, request):

        location_id = request.POST.get('location')

        location = Location.objects.get(id=location_id)

        if location:
            location.delete()

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminCreateSport(View):
    def post(self, request):
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        sport_type = request.POST.get('type')
        coord_id = request.POST.get('coordinator')

        coordinator = Person.objects.get(id=coord_id)

        sport = Sport(
            name=name, gender=gender, sport_type=sport_type, coordinator=coordinator
        )

        sport.save()

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminDeleteSport(View):
    def post(self, request):

        sport_id = request.POST.get('sport')

        sport = Sport.objects.get(id=sport_id)

        if sport:
            sport.delete()

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)
