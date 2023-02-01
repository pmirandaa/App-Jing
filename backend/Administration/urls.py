from django.urls import path

from Administration.views import AdminPanelView
from Administration.views import AdminCreatePerson, AdminEditPerson, AdminDeletePerson
from Administration.views import AdminCreateUniversity, AdminEditUniversity, AdminDeleteUniversity
from Administration.views import AdminCreateLocation, AdminEditLocation, AdminDeleteLocation
from Administration.views import AdminCreateSport, AdminEditSport, AdminDeleteSport
from Administration.views import _uploadPersonData
app_name = 'administration'

urlpatterns = [
    path('admin', AdminPanelView.as_view(), name='administracion-section'),
    path('create-user', AdminCreatePerson.as_view(), name='crear-usuario'),
    path('edit-user', AdminEditPerson.as_view(), name='editar-usuario'),
    path('delete-user', AdminDeletePerson.as_view(), name='borrar-usuario'),
    path('create-university', AdminCreateUniversity.as_view(),
         name='crear-universidad'),
    path('edit-university', AdminEditUniversity.as_view(),
         name='editar-universidad'),
    path('delete-university', AdminDeleteUniversity.as_view(),
         name='borrar-universidad'),
    path('create-location', AdminCreateLocation.as_view(),
         name='crear-lugar'),
    path('edit-location', AdminEditLocation.as_view(),
         name='editar-lugar'),
    path('delete-location', AdminDeleteLocation.as_view(),
         name='borrar-lugar'),
    path('create-sport', AdminCreateSport.as_view(),
         name='crear-deporte'),
    path('edit-sport', AdminEditSport.as_view(),
         name='editar-deporte'),
    path('delete-sport', AdminDeleteSport.as_view(),
         name='borrar-deporte'),
    path('upload-data', _uploadPersonData, name='subir-datos'),
]
