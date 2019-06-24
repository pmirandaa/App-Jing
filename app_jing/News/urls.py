from django.urls import path
from django.views.generic import TemplateView

from News.views import HomeNews

app_name = 'news'

urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
]
