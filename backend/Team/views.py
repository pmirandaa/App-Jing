from time import sleep
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.utils import is_valid_param

from Team.models import Team, PlayerTeam
from Team.serializers import TeamSerializer, PlayerTeamSerializer, TeamTestSerializer
from Sport.models import Sport
from University.models import University


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
           return  TeamTestSerializer
        else:
            return TeamSerializer

    def dispatch(self, request, *args, **kwargs):
       
        sleep(0.5)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        event = self.request.query_params.get('event')
        sport = self.request.query_params.get('sport')
        university = self.request.query_params.get('university')
        gender = self.request.query_params.get('gender')
        sport_type = self.request.query_params.get('sport_type')
        if is_valid_param(event):
            queryset = queryset.filter(event__exact=event)
        if is_valid_param(sport):
            queryset = queryset.filter(sport__exact=sport)
        if is_valid_param(university):
            queryset = queryset.filter(university__exact=university)
        if is_valid_param(gender):
            queryset = queryset.filter(sport__gender__exact=gender)
        if is_valid_param(sport_type):
            queryset = queryset.filter(sport__sport_type__exact=sport_type)
        queryset = queryset.order_by('sport')
        return queryset

    @method_decorator(cache_page(60))
    @action(detail=False)
    def filters(self, request):
        data = {}
        event = self.request.query_params.get('event')
        if is_valid_param(event):
            universities = University.objects.filter(
                universityevent__event__exact=event).values('pk', 'short_name')
            data["universities"] = [
                {"value": x["pk"], "label": x["short_name"]} for x in universities]
            sports = Sport.objects.all().values('pk', 'name')
            data["sport"] = [{"value": x["pk"], "label": x["name"]}
                             for x in sports]
            data["gender"] = [{"value": x[0], "label": x[1]}
                              for x in Sport.SPORT_GENDER]
            data["sport_type"] = [{"value": x[0], "label": x[1]}
                                  for x in Sport.SPORT_TYPE]
        return Response(data)


class PlayerTeamViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerTeamSerializer
    queryset = PlayerTeam.objects.all()
