from django.urls import path

from Sport.views import GetScoresView
from Sport.views import CloseChampionshipView

app_name = 'sport'

urlpatterns = [
    path('get-scores', GetScoresView.as_view(), name='scores'),
    path('close-champ', CloseChampionshipView.as_view(), name='close-championship'),
]