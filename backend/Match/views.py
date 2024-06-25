from datetime import datetime
from time import sleep
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.db.models import Count

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.utils import is_valid_param, bool_param

from Person.models import getPersonEventRoles, Person  
from Team.models import Team, PlayerTeam
from Location.models import Location
from Match.models import Match, MatchTeam
from Sport.models import Sport
from Event.models import Event
from University.models import University
from .exceptions import MatchAlreadyPlayed, MatchAlreadyClosed, MatchNotPlayed
from .serializers import MatchInfoSerializer, MatchStatusSerializer, MatchCreateSerializer, MatchUpdateSerializer
import json


class MatchViewSet(ModelViewSet):
    read_serializer_class = MatchInfoSerializer
    create_serializer_class = MatchCreateSerializer
    update_serializer_class = MatchUpdateSerializer
    status_serializer_class = MatchStatusSerializer
    queryset = Match.objects.all()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            serializer_class = self.create_serializer_class
        elif self.action in ['update', 'partial_update']:
            serializer_class = self.update_serializer_class
        else:
            serializer_class = self.read_serializer_class
        return serializer_class

    def get_queryset(self):
        queryset = self.queryset
        qp = self.request.query_params
        event = qp.get('event')
        my_matches = qp.get('my_matches')
        participants = qp.get('participants')
        sport = qp.get('sport')
        location = qp.get('location')
        played = bool_param(qp.get('played'))
        closed = bool_param(qp.get('closed'))
        if is_valid_param(event):
            queryset = queryset.filter(event=event)
        if is_valid_param(my_matches):
            user = self.request.user
            queryset = queryset.filter(
                match_teams__team__playerteam__player=user.id)
        if is_valid_param(participants):
            participants_list = participants.split(',')
            queryset = queryset.filter(match_teams__team__university__in=participants_list).annotate(
                num_participants=Count('match_teams')).filter(num_participants=len(participants_list))
        if is_valid_param(played):
            queryset = queryset.filter(played=played)
        if is_valid_param(sport):
            queryset = queryset.filter(sport=sport)
        if is_valid_param(location):
            queryset = queryset.filter(location=location)
        if is_valid_param(closed):
            queryset = queryset.filter(closed=closed)
        queryset = queryset.order_by('date')
        return queryset

    @action(detail=True, methods=['POST'])
    def finish(self, request, pk):
        match = self.get_object()
        if match.closed:
            raise MatchAlreadyClosed()
        if match.played:
            raise MatchAlreadyPlayed()
        data = {'played': True, 'time_finished': datetime.now()}
        data = {**request.data, **data}
        data.pop('closed', None)
        serializer = self.status_serializer_class(
            match, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def close(self, request, pk):
        match = self.get_object()
        if match.closed:
            raise MatchAlreadyClosed()
        if not match.played:
            raise MatchNotPlayed()

        data = {'closed': True}
        if not match.time_finished:
            data['time_finished'] = datetime.now()

        data = {**request.data, **data}
        serializer = self.status_serializer_class(
            match, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

    @method_decorator(cache_page(60))
    @action(detail=False)
    def filters(self, request):
        data = {}
        event = self.request.query_params.get('event')
        if is_valid_param(event):
            participants = University.objects.filter(
                universityevent__event__exact=event).values('pk', 'short_name')
            data["participants"] = [
                {"value": x["pk"], "label": x["short_name"]} for x in participants]
            sports = Sport.objects.all().values('pk', 'name')
            data["sport"] = [{"value": x["pk"], "label": x["name"]}
                             for x in sports]
            data["gender"] = [{"value": x[0], "label": x[1]}
                              for x in Sport.SPORT_GENDER]
            data["sport_type"] = [{"value": x[0], "label": x[1]}
                                  for x in Sport.SPORT_TYPE]
            locations = Location.objects.all().values('pk', 'name')
            data["location"] = [{"value": x["pk"], "label": x["name"]}
                                for x in locations]
            #data["participants"] = UniversityEvent.objects.filter(event=event).values_list('university', flat=True)
        return Response(data)
    
@require_POST
def CreateMatch(request):
    eventid= request.POST["event"]
    print(eventid)
    event=Event.objects.get(pk=eventid)
    roles=getPersonEventRoles(request.user.person,event)
    print(request.user.is_authenticated) 
    if (request.user.is_authenticated  and 'organizador' in roles) or "admin" in roles:
        name=request.POST["name"]
        print("name " +name)
        sportid = request.POST["sport"]
        sport= Sport.objects.get(pk=sportid)
        print("sport" )
        print( sport)
        eventid=request.POST["event"]
        event=Event.objects.get(pk=eventid)
        print("event")
        print( event)
        teamslist=request.POST["teams"]
        teams =json.loads(teamslist)
        print("teams")
        print(teams)
        locationid=request.POST["location"]
        location= Location.objects.get(pk=locationid)
        print("location" )
        print(location)
        date=request.POST["date"]
        print(date)

        match=Match.objects.create(name=name, sport=sport, event=event,date=date, location=location)
        for element in teams:
            team= Team.objects.get(pk=element["value"])
            p=MatchTeam.objects.create(team=team, match=match)
            print(p)

        return JsonResponse({"detail": "Partido Creado"})

    print("Sin autenticar")
    return JsonResponse({"detail": "Not authenticated"})


@require_POST
def CreateResult(request):
    eventid= request.POST["event"]
    print(eventid)
    event=Event.objects.get(pk=eventid)
    roles=getPersonEventRoles(request.user.person,event)
    print(request.user.is_authenticated) 
    if (request.user.is_authenticated  and 'organizador' in roles) or "admin" in roles:
        post =request.POST
        print(post)
        matchid = post['match']
        match = Match.objects.filter(pk=matchid)
        print("match var")
        print(match)
        teamScore = post['teamScore']
        teamScore=json.loads(teamScore)
        winners_list= post['winners']
        winners=json.loads(winners_list)
        #for team in winners:
         #   print(team)
          #  winners.append(team["value"])
        print(winners)
        played=post['played']
        if(played=="true"):
            played=True
        else:
            played=False
        closed= post['closed']
        if(closed=="true"):
            closed=True
        else:
            closed=False
        
        attendance_list= post['attendance']
        attendance=json.loads(attendance_list)
        
        # initializing the lists in Python to use lambda and map.
        # the first step will be printing the string value
        ##print("Original list : ", winners)

        # now using the map() method in Python to extend as well as the lambda function to check "True" string
        ##winners = list(map(lambda element1: element1.lower().
          ##          capitalize() == "True", winners))
        
        ##print("list result", winners)

        try:
            print(teamScore) 
            match_update_fields={'played':played, 'closed':closed}     
            a = match.update(**match_update_fields)
            print(a)
            print(type(teamScore))

            for team in teamScore:
                print(team)
                t= Team.objects.get(pk=team)
                print(t)
                matchteam_update_fields={'score':int(teamScore[team]),'attended':  attendance[team]}
                print(matchteam_update_fields)
                mt = MatchTeam.objects.filter(team=t, match=match.get()).update(**matchteam_update_fields)
                print(t)
                print("t id")
                print(t.id)
                if(t.id in winners):
                    print("actualizando ganadores")
                    matchteam_update_fields={'is_winner':True}
                    mt = MatchTeam.objects.filter(team=t, match=match.get()).update(**matchteam_update_fields)
                    print(winners)
            
            return JsonResponse({'detail': 'Resultado Creado'})
                    
        except ValueError as e:
            return JsonResponse({'Error': str(e)})
      
