from django.db import models
from Event.models import Event
from Person.models import Person

# agregar un dueño al canal o algo asi
class Chat(models.Model):
    name= models.CharField(max_length=20)
    event= models.ForeignKey(Event, on_delete=models.CASCADE)
    is_active= models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

class Message(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sender')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')
    #reciever = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='reciever')
    #event = models.ForeignKey(Event, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} --> {self.chat} -- {self.subject}'

class ChatPerson(models.Model):
    person= models.ForeignKey(Person, on_delete=models.CASCADE)
    chat= models.ForeignKey(Chat,on_delete=models.CASCADE)

def PersonsChats(person):
    names= ChatPerson.objects.filter(person=person).values_list('chat__name', flat=True)
    ids=  ChatPerson.objects.filter(person=person).values_list('chat', flat=True)
    print("en persons chat")
    print(names)
    return names, ids
