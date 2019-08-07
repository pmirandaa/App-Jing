from django.urls import path
from django.views.generic import TemplateView

from Administration.views import AdminPanel
from Administration.views import AdminCreateUser, AdminDeleteUser
from Administration.views import AdminCreateUniversity, AdminDeleteUniversity
from Administration.views import AdminCreateLocation, AdminDeleteLocation
from Administration.views import AdminCreateSport, AdminDeleteSport

app_name = 'administration'

urlpatterns = [
    path('', AdminPanel.as_view(), name='administracion-section'),
    path('create-user', AdminCreateUser.as_view(), name='crear-usuario'),
    path('delete-user', AdminDeleteUser.as_view(), name='borrar-usuario'),
    path('create-university', AdminCreateUniversity.as_view(),
         name='crear-universidad'),
    path('delete-university', AdminDeleteUniversity.as_view(),
         name='borrar-universidad'),
    path('create-location', AdminCreateLocation.as_view(),
         name='crear-lugar'),
    path('delete-location', AdminDeleteLocation.as_view(),
         name='borrar-lugar'),
    path('create-sport', AdminCreateSport.as_view(),
         name='crear-deporte'),
    path('delete-sport', AdminDeleteSport.as_view(),
         name='borrar-deporte'),
]
