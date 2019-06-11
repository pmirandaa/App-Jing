from django.urls import path
from django.views.generic import TemplateView

from Person.views import RegisterView
from Person.views import LoginView
from Person.views import LogoutView

app_name = 'person'

urlpatterns = [
    path('', TemplateView.as_view(
        template_name="Inicio/baseInicio.html"), name='non-auth-home'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
