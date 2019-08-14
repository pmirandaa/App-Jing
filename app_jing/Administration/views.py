from django.shortcuts import render
from django.views import View

from django.http.response import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse

from Person.models import Person
from Event.models import Event
from University.models import University
from Location.models import Location
from Sport.models import Sport


class AdminPanel(View):

    def get(self, request):

        person = None
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
                          "unis_coords": unis_coords,
                          "alert": request.session.pop('alert', None)
                      })


class AdminCreatePerson(View):

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

        person = Person(
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
            request.session['alert'] = {
                'type': 'success',
                'message': 'Usuario creado exitosamente'
            }
        except:
            person.delete()
            request.session['alert'] = {
                'type': 'danger',
                'message': 'Ocurrió un error al crear el usuario'
            }

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminEditPerson(View):
    def get(self, request):
        person_id = request.GET.get('id')
        unis = University.objects.all()
        events = Event.objects.all()

        person = Person.objects.get(id=person_id)

        if person:
            return render(request, 'Administration/editPerson.html',
                          {
                              "person": person,
                              "universities": unis,
                              "events": events
                          })

        return HttpResponseNotFound()

    def post(self, request):
        person_id = request.POST.get('id')
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

        person = Person.objects.get(id=person_id)

        if person:
            person.event = event
            person.name = nombres
            person.last_name = apellidos
            person.email = email
            person.university = university
            person.rut = rut
            person.phone_number = phone
            person.is_admin = is_admin
            person.is_organizer = is_organizer
            person.is_university_coordinator = is_university_coordinator
            person.is_sports_coordinator = is_sports_coordinator

            try:
                person.save()
                request.session['alert'] = {
                    'type': 'info',
                    'message': 'Usuario editado exitosamente'
                }
            except:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al editar el usuario'
                }

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminDeletePerson(View):
    def post(self, request):

        person_id = request.POST.get('user')

        person = Person.objects.get(id=person_id)

        myself = None
        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                myself = Person.objects.get(user=request.user)

        if person:
            if person != myself:
                person.delete()
                request.session['alert'] = {
                    'type': 'info',
                    'message': 'Usuario eliminado exitosamente'
                }
            else:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'No puedes eliminarte a ti mismo'
                }
        else:
            request.session['alert'] = {
                'type': 'warning',
                'message': 'No se ha encontrado el usuario a eliminar'
            }

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

        try:
            university.save()
            request.session['alert'] = {
                'type': 'success',
                'message': 'Universidad creada exitosamente'
            }
        except:
            request.session['alert'] = {
                'type': 'danger',
                'message': 'Ocurrió un error al crear la universidad'
            }
            university.delete()

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminEditUniversity(View):
    def get(self, request):
        uni_id = request.GET.get('id')
        uni = University.objects.get(id=uni_id)

        if uni:
            return render(request, 'Administration/editUniversity.html',
                          {
                              "university": uni
                          })

        return HttpResponseNotFound()

    def post(self, request):
        uni_id = request.POST.get('id')
        name = request.POST.get('name')
        city = request.POST.get('city')
        short_name = request.POST.get('short-name')

        uni = University.objects.get(id=uni_id)

        if uni:
            uni.name = name
            uni.city = city
            uni.short_name = short_name

            try:
                uni.save()
                request.session['alert'] = {
                    'type': 'info',
                    'message': 'Universidad editada exitosamente'
                }
            except:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al actualizar la universidad'
                }

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminDeleteUniversity(View):
    def post(self, request):

        uni_id = request.POST.get('university')

        university = University.objects.get(id=uni_id)

        if university:
            try:
                university.delete()
                request.session['alert'] = {
                    'type': 'info',
                    'message': 'Universidad eliminada exitosamente'
                }
            except:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al eliminar la universidad'
                }

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

        try:
            location.save()
            request.session['alert'] = {
                'type': 'success',
                'message': 'Lugar creado exitosamente'
            }
        except:
            location.delete()
            request.session['alert'] = {
                'type': 'danger',
                'message': 'Ocurrió un error al crear el lugar'
            }

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminEditLocation(View):
    def get(self, request):
        location_id = request.GET.get('id')
        location = Location.objects.get(id=location_id)

        unis = University.objects.all()

        if location:
            return render(request, 'Administration/editLocation.html',
                          {
                              "universities": unis,
                              "location": location
                          })

        return HttpResponseNotFound()

    def post(self, request):
        location_id = request.POST.get('id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        uni_id = request.POST.get('university')

        university = University.objects.get(id=uni_id)
        location = Location.objects.get(id=location_id)
        if university and location:

            location.name = name
            location.address = address
            location.university = university

            try:
                location.save()
                request.session['alert'] = {
                    'type': 'info',
                    'message': 'Lugar editado exitosamente'
                }
            except:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al editar el lugar'
                }

            redirect_url = reverse('administration:administracion-section')
            return HttpResponseRedirect(redirect_url)

        return HttpResponseNotFound()


class AdminDeleteLocation(View):
    def post(self, request):

        location_id = request.POST.get('location')

        location = Location.objects.get(id=location_id)

        if location:
            try:
                location.delete()
                request.session['alert'] = {
                    'type': 'info',
                    'message': 'Lugar eliminado exitosamente'
                }
            except:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al eliminar el lugar'
                }

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

        try:
            sport.save()
            request.session['alert'] = {
                'type': 'success',
                'message': 'Deporte creado exitosamente'
            }
        except:
            sport.delete()
            request.session['alert'] = {
                'type': 'danger',
                'message': 'Ocurrió un error al crear el deporte'
            }

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)


class AdminEditSport(View):
    def get(self, request):
        sport_id = request.GET.get('id')
        sport = Sport.objects.get(id=sport_id)

        sport_coords = Person.objects.filter(is_sports_coordinator=True)
        sport_types = Sport.SPORT_TYPE
        genders = Sport.SPORT_GENDER

        if sport:
            return render(request, 'Administration/editSport.html',
                          {
                              "sports_coords": sport_coords,
                              "sport": sport,
                              "sport_types": sport_types,
                              "genders": genders
                          })

        return HttpResponseNotFound()

    def post(self, request):
        sport_id = request.POST.get('id')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        sport_type = request.POST.get('type')
        coord_id = request.POST.get('coordinator')

        sport = Sport.objects.get(id=sport_id)
        coordinator = Person.objects.get(id=coord_id)

        if sport and coordinator:
            sport.name = name
            sport.gender = gender
            sport.sport_type = sport_type
            sport.coordinator = coordinator

            try:
                sport.save()
                request.session['alert'] = {
                    'type': 'info',
                    'message': 'Deporte editado exitosamente'
                }
            except:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al editar el deporte'
                }

            redirect_url = reverse('administration:administracion-section')
            return HttpResponseRedirect(redirect_url)

        return HttpResponseNotFound()


class AdminDeleteSport(View):
    def post(self, request):

        sport_id = request.POST.get('sport')

        sport = Sport.objects.get(id=sport_id)

        if sport:
            try:
                sport.delete()
                request.session['alert'] = {
                    'type': 'info',
                    'message': 'Deporte elimnado exitosamente'
                }
            except:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al eliminar el deporte'
                }

        redirect_url = reverse('administration:administracion-section')
        return HttpResponseRedirect(redirect_url)
