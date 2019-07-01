from django.urls import path
from django.views.generic import TemplateView

app_name = 'administration'

urlpatterns = [
    path('', TemplateView.as_view(
        template_name="Administration/baseAdmin.html"), name='administracion-section'),
]
