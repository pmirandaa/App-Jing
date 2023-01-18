"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from rest_framework import routers

from Administration.views import LogViewSet
from Authentication.views import UserViewSet
from Event.views import EventViewSet
from Location.views import LocationViewSet
from Match.views import MatchViewSet
from Message.views import MessageViewSet
from News.views import NewsViewSet, NewsCategoryViewSet
from Person.views import PersonViewSet
from Placement.views import EventPlacementViewSet, SportPlacementViewSet
from Sport.views import SportViewSet, FinalSportPointsViewSet
from Team.views import TeamViewSet, PlayerTeamViewSet
from University.views import UniversityViewSet


router = routers.DefaultRouter()
router.register('logs', LogViewSet, 'logs')
router.register('events', EventViewSet, 'events')
router.register('locations', LocationViewSet, 'locations')
router.register('matches', MatchViewSet, 'matches')
router.register('messages', MessageViewSet, 'messages')
router.register('news', NewsViewSet, 'news')
router.register('news_categories', NewsCategoryViewSet, 'news_categories')
router.register('persons', PersonViewSet, 'persons')
router.register('sports', SportViewSet, 'sports')
router.register('final_sport_points', FinalSportPointsViewSet, 'final_sport_points')
router.register('teams', TeamViewSet, 'teams')
router.register('player_teams', PlayerTeamViewSet, 'player_teams')
router.register('universities', UniversityViewSet, 'universities')
router.register('users', UserViewSet, 'users')
router.register('placements/event', EventPlacementViewSet, 'event_placements')
router.register('placements/sport', SportPlacementViewSet, 'sport_placements')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
