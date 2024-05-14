from django.urls import path

#from Message.views import HomeMessages
#from Message.views import ReadMessages
from Message.views import getPersonsChats, createNewChat

app_name = 'messages'

urlpatterns = [
    #path('', HomeMessages.as_view(), name='home'),
    #path('read_mesages/', ReadMessages.as_view(), name='read'),
    path('getpersonschats/', getPersonsChats, name='chats'),
    path('createnewchat/', createNewChat, name='createnewchat')
]
