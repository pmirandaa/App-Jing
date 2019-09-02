from django.urls import path
from django.views.generic import TemplateView

from News.views import HomeNews
from News.views import CreateNews

app_name = 'news'

urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
    path('create', CreateNews.as_view(), name='create')
]
