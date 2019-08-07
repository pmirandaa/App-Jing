from django.shortcuts import render
from django.views import View

from django.http.response import HttpResponseRedirect
from django.urls import reverse

from datetime import datetime

from Location.models import Location
from Person.models import Person
from Team.models import Team
from Match.models import Match, MatchTeam
from Sport.models import Sport

# Create your views here.


class MatchView(View):
    def get(self, request):

        person = None
        event = None
        teams = None
        # TODO: Filtrar ambos por evento
        pending_matches = Match.objects.exclude(state=Match.PLAYED)
        played_matches = Match.objects.filter(state=Match.PLAYED)

        locations = Location.objects.all()
        sports = Sport.objects.all()

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)
                event = person.event
                teams = Team.objects.filter(event=event)

                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(
                        person=person).latest()
        return render(request, 'Match/baseMatch.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "pending": pending_matches,
                          "played": played_matches,
                          "locations": locations,
                          "sports": sports,
                          "teams": teams
                      })

    def post(self, request):

        sport_id = request.POST.get('sport')
        teams = request.POST.getlist('team[]')
        length = request.POST.get('length')
        location_id = request.POST.get('location')

        date = request.POST.get('date')
        time = request.POST.get('time')
        dt = '{} {}'.format(date, time)

        match_date = datetime.strptime(dt, "%d-%m-%Y %H:%M")
        event = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)
                event = person.event

        if len(teams) >= 2 and event is not None:
            sport = Sport.objects.get(id=sport_id)
            location = Location.objects.get(id=location_id)

            match = Match(
                location=location,
                sport=sport,
                event=event,
                length=length,
                date=match_date
            )
            match.save()
            match_teams = []
            for team_id in teams:
                team = Team.objects.get(id=team_id)
                if team is not None:
                    match_team = MatchTeam(team=team)
                    match_team.save()
                    match.teams.add(match_team)

                else:
                    for mt in match_teams:
                        mt.delete()
                    match.delete()

        redirect_url = reverse('match:matches-section')
        return HttpResponseRedirect(redirect_url)


class MatchStartView(View):
    def post(self, request):
        match_id = request.POST.get('match')

        match = Match.objects.get(id=match_id)

        if match is not None:
            match.state = Match.PLAYING
            match.save()

        redirect_url = reverse('match:matches-section')
        return HttpResponseRedirect(redirect_url)


class MatchFinishView(View):

    def get(self, request):
        match_id = request.GET.get('match')

        match = Match.objects.get(id=match_id)

        return render(request, 'Match/finishMatch.html',
                      {
                          "match": match
                      })

    def post(self, request):
        match_id = request.POST.get('match')
        winner_id = request.POST.get('winner')

        match = Match.objects.get(id=match_id)

        if match is not None:
            for mt in match.teams.all():
                team_id = mt.team.id
                score_name = 'score-{}'.format(team_id)
                score = request.POST.get(score_name)
                if score != '':
                    mt.score = score
                    mt.save()
                else:
                    redirect_url = reverse('match:matches-section')
                    return HttpResponseRedirect(redirect_url)

            match.state = Match.PLAYED
            winner = Team.objects.get(id=winner_id)
            tm_winner = match.teams.get(team=winner)
            tm_winner.winner = True
            tm_winner.save()
            match.save()

        redirect_url = reverse('match:matches-section')
        return HttpResponseRedirect(redirect_url)


class MatchCloseView(View):

    def get(self, request):
        match_id = request.GET.get('match')

        match = Match.objects.get(id=match_id)

        return render(request, 'Match/closeMatch.html',
                      {
                          "match": match
                      })

    def post(self, request):
        match_id = request.POST.get('match')
        winner_id = request.POST.get('winner')

        match = Match.objects.get(id=match_id)

        if match is not None:
            for mt in match.teams.all():
                team_id = mt.team.id
                score_name = 'score-{}'.format(team_id)
                score = request.POST.get(score_name)
                if score != '':
                    mt.score = score
                    mt.save()
                else:
                    redirect_url = reverse('match:matches-section')
                    return HttpResponseRedirect(redirect_url)

            match.state = Match.PLAYED
            match.closed = True
            winner = Team.objects.get(id=winner_id)
            tm_winner = match.teams.get(team=winner)
            tm_winner.winner = True
            tm_winner.save()
            match.save()

        redirect_url = reverse('match:matches-section')
        return HttpResponseRedirect(redirect_url)


class MatchResultsView(View):

    def get(self, request):
        match_id = request.GET.get('match')

        match = Match.objects.get(id=match_id)

        return render(request, 'Match/resultsMatch.html',
                      {
                          "match": match
                      })


class MatchDeleteView(View):
    def post(self, request):
        match_id = request.POST.get('match')

        match = Match.objects.get(id=match_id)
        match.teams.all().delete()

        if match is not None:
            match.delete()

        redirect_url = reverse('match:matches-section')
        return HttpResponseRedirect(redirect_url)
