from django.urls import path

from Person.views import RegisterView
from Person.views import LoginView
from Person.views import LogoutView
from Person.views import HomePerson
from Person.views import UnvalidatedPerson
from Person.views import GetQRAndCode
from Person.views import ValidateUser

app_name = 'person'

urlpatterns = [
    path('', HomePerson.as_view(), name='non-auth-home'),
    path('get_unvalidated/', UnvalidatedPerson.as_view(), name='unvalidated'),
    path('get_qr/', GetQRAndCode.as_view(), name='getcodes'),
    path('validate/', ValidateUser.as_view(), name='validate'),
    path('validate/<int:person_id>', ValidateUser.as_view()),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
