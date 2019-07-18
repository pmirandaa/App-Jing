from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect

from django.views import View
from django.urls import reverse
from django.shortcuts import render

from Person.models import Person
from Person.models import PersonAvatar

from Message.models import Message

from University.models import University

import ast


class HomeMessages(View):

  def get(self, request):
    person = None
    avatar = None

    if request.user.is_authenticated:
        if Person.objects.filter(user=request.user).exists():
            person = Person.objects.get(user=request.user)

            if person.has_avatar:
                avatar = PersonAvatar.objects.filter(person=person).latest()

    messages = Message.objects.filter(
      reciever__user=request.user, deleted=False).order_by('-date')

    unread_messages_ids = list(messages.filter(is_read=False).values_list('id', flat=True))

    universities = University.objects.all()

    return render(request, 'Mensajes/baseMensajes.html',
                  {
                      "name": request.user.username,
                      "person": person,
                      "avatar": avatar,
                      "messages": messages,
                      "unread_messages": unread_messages_ids,
                      "universities": universities
                  })


class ReadMessages(View):

    def post(self, request):
        ids = ast.literal_eval(request.POST.get('unread_messages'))

        Message.objects.filter(pk__in=ids).update(is_read=True)

        return HttpResponse({})
