from django.urls import path
from .views import UserViewSet

app_name = 'Authentication'
urlpatterns = [
    path('register/', UserViewSet.as_view({'get' : 'list'}), name='register'),
]