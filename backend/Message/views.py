from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect

from django.views import View
from django.urls import reverse
from django.shortcuts import render

from rest_framework import viewsets

from Person.models import Person

from Message.models import Message
from Message.serializers import MessageSerializer
from Event.models import Event

from University.models import University
from Team.models import Team
from Team.models import PlayerTeam
from Sport.models import Sport

import json
import ast

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

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
        teams = Team.objects.all()
        sports = Sport.objects.all()

        return render(request, 'Mensajes/baseMensajes.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "avatar": avatar,
                          "messages": messages,
                          "unread_messages": unread_messages_ids,
                          "universities": universities,
                          "teams": teams,
                          "sports": sports,
                      })

    def post(self, request):
        universities = request.POST.getlist('universities[]', None)
        teams = request.POST.getlist('teams[]', None)
        sports = request.POST.getlist('sports[]', None)
        people = request.POST.getlist('people[]', None)

        subject = request.POST.get('subject')
        message_body = request.POST.get('message')

        message_recievers = []

        if universities is not None:
            university_recievers = list(Person.objects.filter(university_id__in=universities).values_list('id', flat=True))
            
            message_recievers.extend(university_recievers)

        if teams is not None:
            team_recievers = list(PlayerTeam.objects.filter(team_id__in=teams).values_list('player_id', flat=True))
            
            message_recievers.extend(team_recievers)

        if sports is not None:
            sport_recievers = list(PlayerTeam.objects.filter(team__sport_id__in=sports).values_list('player_id', flat=True))
            
            message_recievers.extend(sport_recievers)

        if people is not None:
            for person in people:
                message_recievers.append(Person.objects.filter(name__iexact=person).first().id)

        message_recievers = list(dict.fromkeys(message_recievers))

        sender = Person.objects.get(user=request.user)
        event = Event.objects.all().first()
        reload = False

        for message_reciever in message_recievers:
            reciever = Person.objects.get(pk=message_reciever)

            message = Message(
                sender=sender,
                reciever=reciever,
                event=event,
                subject=subject,
                body=message_body,
            )

            message.save()

            reciever.pending_messages += 1
            reciever.save()

            if reciever.id == sender.id:
                reload = True

        if reload:
            return_message = f'Enviados {len(message_recievers)} mensajes, la pagina se recargara en breve'
        else:
            return_message = f'Enviados {len(message_recievers)} mensajes'

        return HttpResponse(json.dumps({
            "message": return_message,
            "reload": reload
        }))


class ReadMessages(View):

    def post(self, request):
        ids = ast.literal_eval(request.POST.get('unread_messages'))

        for id in ids:
            message = Message.objects.get(pk=id)
            reciever = message.reciever

            reciever.pending_messages -= 1
            reciever.save()

            message.is_read = True
            message.save()

        return HttpResponse({})
