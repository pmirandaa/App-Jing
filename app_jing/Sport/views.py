from django.shortcuts import render

from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect

from django.urls import reverse

from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q

from django.views import View

from Team.models import Team
from Match.models import Match
from Match.models import MatchTeam
from Sport.models import Sport
from Sport.models import FinalSportPoints
from University.models import University

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

        for key, value in places.items():
            final_place[key] = {
                'place': key,
                'team_name': str(Team.objects.get(pk=value[0]).university),
                'matches_won': value[1],
                'overall_points': MatchTeam.objects.filter(team_id=value[0]).aggregate(Sum('score'))['score__sum'],
                'id': value[0]
            }

        return render(request, "Team/closeChampionship.html", {"places": final_place})

    def post(self, request):
        first_place = 1
        iterate = True
        sport_id = None

        while iterate:
            place = request.POST.get(f'place_{first_place}')
            id = request.POST.get(f'id_{first_place}')

            if place is None:
                iterate = False
                break
            
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

        return HttpResponseRedirect(reverse('administration:administracion-section'))
            
            
