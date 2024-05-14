from rest_framework import viewsets
from utils import bool_param, is_valid_param
from django.http import JsonResponse, HttpResponse

from Message.models import Message, Chat, PersonsChats, ChatPerson
from Person.models import Person
from Event.models import Event
from Message.serializers import MessageSerializer, ChatSerializer
import json 


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    
    def get_queryset(self):
        empty = Message.objects.none()
        if self.request.user.is_authenticated:
            person =self.request.user.person
            personchats, ids= PersonsChats(person)
            queryset = self.queryset
            sender = self.request.query_params.get('sender')
            chat = self.request.query_params.get('chat')
            is_read = self.request.query_params.get('is_read')
            date = self.request.query_params.get('date')
            print(sender)
            print(is_valid_param(sender))
            print(chat)
            if int(chat) in ids:
                if is_valid_param(sender):
                    queryset = queryset.filter(sender__rut=sender)
                if is_valid_param(chat):
                    queryset = queryset.filter(chat__id=chat)
                if is_valid_param(is_read):
                    queryset = queryset.filter(is_read=is_read)
                if is_valid_param(date):
                    queryset = queryset.filter(date=date)
                return queryset
            else:
                return empty
        else:
            return empty

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')
        event = self.request.query_params.get('event')
        is_active = self.request.query_params.get('is_active')
        if is_valid_param(name):
            queryset = queryset.filter(name=name)
        if is_valid_param(event):
            queryset = queryset.filter(event=event)
        if is_valid_param(is_active):
            queryset = queryset.filter(is_active=is_active)
        return queryset
    

def getPersonsChats(request):
    print("get personaschats funcions")
    person =request.user.person
    names, ids = PersonsChats(person)
    names=list(names)
    ids=list(ids)
    print(names, ids)
    lista=[]
    data=Chat.objects.filter(pk__in=ids) #lo ideal seria enviar una lista de diccionarios con el nombre y el id del chat
    #queryset = queryset.filter(playerteam__team__sport=sport) [{id:1, nombre:'chat'}]
    data=list(data)
    i=0
    for name in names:
        objeto={'id':ids[i], 'name':name}
        lista.append(objeto)
        print(lista)
        i=i+1
    return JsonResponse({"detail": lista})

def createNewChat(request):
    admins=[] #añadie despues los usuairo admins
    persons=[]
    event=0
    name=""

    post=request.POST
    personlist= request.POST["persons"]
    name= request.POST["name"]
    eventid= request.POST["event"]
    print(post)
    print(personlist[0])
    jsonloads=json.loads(personlist)
    print(jsonloads)
    print(jsonloads[0]["label"])

    event= Event.objects.get(pk=eventid)
    chat=Chat.objects.create(name=name, event=event)
    
    for element in jsonloads:
        person= Person.objects.get(pk=element["value"])
        p=ChatPerson.objects.create(person=person, chat=chat)
        print(p)
    
    return JsonResponse({"detail": "chat creado"})
        

