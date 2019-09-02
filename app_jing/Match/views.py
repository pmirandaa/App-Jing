from datetime import datetime
from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from django.views import View

from django.http.response import HttpResponseRedirect
from django.urls import reverse

from Location.models import Location
from Person.models import Person
from Team.models import Team
from Match.models import Match, MatchTeam
from Sport.models import Sport
from Administration.models import Log

# Create your views here.


class MatchView(View):
    def get(self, request):

        person = None
        event = None
        teams = None
        # TODO: Filtrar ambos por evento
        pending_matches = Match.objects.exclude(state=Match.PLAYED)
        played_matches = Match.objects.filter(state=Match.PLAYED)
        
        played_closed_matches = played_matches.filter(time_closed__lt=(timezone.now() - timedelta(hours=1)))
        played_opened_matches = played_matches.filter(time_closed__gt=(timezone.now() - timedelta(hours=1)))

        locations = Location.objects.all()
        sports = Sport.objects.all()

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)
                event = person.event
                teams = Team.objects.filter(event=event)

        return render(request, 'Match/baseMatch.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "pending": pending_matches,
                          "played_closed": played_closed_matches,
                          "played_open": played_opened_matches,
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
        d_t = '{} {}'.format(date, time)

        match_date = datetime.strptime(d_t, "%Y-%m-%d %H:%M")
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
                    for m_t in match_teams:
                        m_t.delete()
                    match.delete()
            doer = Person.objects.get(user=request.user)
            log = Log(
                task = 'create_match',
                value_before = 'None',
                value_after = str(match),
                person= f'{doer.name} {doer.last_name}',
                date= timezone.now()
            )
            log.save()

        redirect_url = reverse('match:matches-section')
        return HttpResponseRedirect(redirect_url)


class MatchStartView(View):
    def post(self, request):
        match_id = request.POST.get('match')

        match = Match.objects.get(id=match_id)

        if match is not None:
            doer = Person.objects.get(user=request.user)
            log = Log(
                task = 'started_match',
                value_before = match.state,
                value_after = Match.PLAYING,
                person= f'{doer.name} {doer.last_name}',
                date= timezone.now()
            )
            log.save()
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
            for m_t in match.teams.all():
                team_id = m_t.team.id
                score_name = 'score-{}'.format(team_id)
                score = request.POST.get(score_name)
                if score != '':
                    m_t.score = score
                    m_t.save()
                else:
                    redirect_url = reverse('match:matches-section')
                    return HttpResponseRedirect(redirect_url)

            doer = Person.objects.get(user=request.user)
            log = Log(
                task = 'finished_match',
                value_before = match.state,
                value_after = Match.PLAYED,
                person= f'{doer.name} {doer.last_name}',
                date= timezone.now()
            )
            log.save()
            match.state = Match.PLAYED
            winner = Team.objects.get(id=winner_id)
            match.winner = winner
            match.time_closed = timezone.now()
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
            for m_t in match.teams.all():
                team_id = m_t.team.id
                score_name = 'score-{}'.format(team_id)
                score = request.POST.get(score_name)
                if score != '':
                    m_t.score = score
                    m_t.save()
                else:
                    redirect_url = reverse('match:matches-section')
                    return HttpResponseRedirect(redirect_url)

            doer = Person.objects.get(user=request.user)
            log = Log(
                task = 'closed_match',
                value_before = match.closed,
                value_after = 'True',
                person= f'{doer.name} {doer.last_name}',
                date= timezone.now()
            )
            log.save()
            match.state = Match.PLAYED
            match.closed = True
            winner = Team.objects.get(id=winner_id)
            match.winner = winner
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


class MatchCommentView(View):

    def get(self, request):
        match_id = request.GET.get('match')

        match = Match.objects.get(id=match_id)

        return render(request, 'Match/commentMatch.html',
                      {
                          "match": match
                      })

    def post(self, request):
        match_id = request.POST.get('match')
        team_id = request.POST.get('team')
        comment = request.POST.get('comment')

        match = Match.objects.get(pk=match_id)
        match_team = match.teams.get(pk=team_id)

        doer = Person.objects.get(user=request.user)
        log = Log(
            task = 'match_add_comment',
            value_before = 'None',
            value_after = comment,
            person= f'{doer.name} {doer.last_name}',
            date= timezone.now()
        )
        log.save()

        match_team.comment = comment
        match_team.save()

        return HttpResponseRedirect(reverse('match:matches-section'))


class MatchDeleteView(View):
    def post(self, request):
        match_id = request.POST.get('match')

        match = Match.objects.get(id=match_id)
        match.teams.all().delete()

        if match is not None:
            doer = Person.objects.get(user=request.user)
            log = Log(
                task = 'match_deleted',
                value_before = str(match),
                value_after = 'None',
                person= f'{doer.name} {doer.last_name}',
                date= timezone.now()
            )
            log.save()
            match.delete()

        redirect_url = reverse('match:matches-section')
        return HttpResponseRedirect(redirect_url)
