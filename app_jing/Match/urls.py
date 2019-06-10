from django.urls import path
from django.views.generic import TemplateView

app_name = 'match'

urlpatterns = [
    path('', TemplateView.as_view(
        template_name="Match/baseMatch.html"), name='matches-section'),
]
