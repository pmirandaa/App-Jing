from django.shortcuts import render

from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect

from django.urls import reverse
from django.utils import timezone

from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q

from django.views import View

from rest_framework import viewsets

from Team.models import Team
from Match.models import Match
from Match.models import MatchTeam
from Sport.models import Sport
from Sport.models import FinalSportPoints
from Sport.serializers import SportSerializer, FinalSportPointsSerializer
from University.models import University
from Person.models import Person
from Administration.models import Log

class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()

class FinalSportPointsViewSet(viewsets.ModelViewSet):
    serializer_class = FinalSportPointsSerializer
    queryset = FinalSportPoints.objects.all()

class GetScoresView(View):

    def get(self, request):
        sport_id = request.GET.get('sport')

        teams = Team.objects.filter(sport_id=sport_id).order_by('place', '-event_score')

        return render(request, 'Team/scoreBoard.html', {'teams': teams})


class CloseChampionshipView(View):

    def get(self, request):
        sport_id = request.GET.get('sport')

        matches = Match.objects.filter(sport_id=sport_id).values('winner').annotate(wins_num=Count('winner'))

        places = {}
        place_initial = 1

        for match in matches:
            
            if match['winner'] is None:
                return HttpResponse('Hay partidos sin terminar para este deporte')

            places[place_initial] = (match['winner'], match['wins_num'])

            place_initial += 1

        places_sorted = dict(sorted(places.items(), key=lambda kv: kv[1][1], reverse=True))
        
        places = {}
        place_initial = 1

        for _, value in places_sorted.items():
            places[place_initial] = value

            place_initial += 1

        
        final_place = {}
        last_place = 1
        unis_with_team = []
        teams_registered = []

        for key, value in places.items():
            team = Team.objects.get(pk=value[0])    
            final_place[key] = {
                'place': key,
                'team_name': str(team.university),
                'matches_won': value[1],
                'overall_points': MatchTeam.objects.filter(team=team).aggregate(Sum('score'))['score__sum'],
                'id': value[0]
            }
            unis_with_team.append(team.university.id)
            teams_registered.append(team.id)
            last_place += 1

        for team in Team.objects.filter(sport_id=sport_id).exclude(id__in=teams_registered):
            final_place[last_place] = {
                'place': last_place,
                'team_name': str(team.university),
                'matches_won': 0,
                'overall_points': MatchTeam.objects.filter(team=team).aggregate(Sum('score'))['score__sum'] or 0,
                'id': team.id
            }
            unis_with_team.append(team.university.id)
            last_place += 1

        for university in University.objects.all().exclude(id__in=unis_with_team):
            final_place[last_place] = {
                'place': last_place,
                'team_name': str(university),
                'matches_won': 0,
                'overall_points': 0,
                'uni_id': university.id
            }
            last_place += 1

        final_place = dict(sorted(final_place.items(), key=lambda kv: kv[1]['overall_points'], reverse=True))
        

        return render(request, "Team/closeChampionship.html", {"places": final_place})

    def post(self, request):
        first_place = 1
        iterate = True
        sport_id = None

        while iterate:
            place = request.POST.get(f'place_{first_place}')
            id = request.POST.get(f'id_{first_place}', None)

            if place is None:
                iterate = False
                break
            
            if id is None:
                print(University.objects.get(pk=request.POST.get(f'uni_id_{first_place}')))
                pass
            
            else:
                team = Team.objects.get(pk=id)
                sport_id = team.sport.id
                team.place = place
                team.event_score = FinalSportPoints.objects.get(sport_type=team.sport.sport_type, place=place).points
                team.save()
                
                uni = University.objects.get(pk=team.university.id)
                uni.overall_score += team.event_score
                uni.save()

            first_place += 1

        sport = Sport.objects.get(pk=sport_id)
        sport.closed = True
        sport.save()
        doer = Person.objects.get(user=request.user)
        log = Log(
            task = 'sport_closed',
            value_before = str(sport),
            value_after = 'closed',
            person= f'{doer.name} {doer.last_name}',
            date= timezone.now()
        )
        log.save()

        return HttpResponseRedirect(reverse('administration:administracion-section'))
            
            
