from django.views import View
from django.shortcuts import render

from Person.models import Person
from Person.models import PersonAvatar


class HomeNews(View):

    def get(self, request):
        person = None
        avatar = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)

                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(person=person).latest()

        return render(request, 'Noticias/baseNoticias.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "avatar": avatar
                      })
