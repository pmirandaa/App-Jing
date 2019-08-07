from django.shortcuts import render
from django.views import View

from django.http.response import HttpResponseRedirect
from django.urls import reverse

from Person.models import Person
from Team.models import Team, PlayerTeam
from Sport.models import Sport
from University.models import University


class TeamHome(View):
    def get(self, request):

        person = None
        teams = Team.objects.all()

        # TODO: Filtrar ambos por evento
        sports = Sport.objects.all()
        universities = University.objects.all()
        players = Person.objects.all()

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)

                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(
                        person=person).latest()
        return render(request, 'Team/baseTeam.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "teams": teams,
                          "sports": sports,
                          "universities": universities,
                          "players": players
                      })

    def post(self, request):
        uni_id = request.POST.get('university')
        sport_id = request.POST.get('sport')
        players = request.POST.getlist('player[]')

        event = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)
                event = person.event

        if len(players) > 0 and event is not None:
            coord_id = players[0]

            coordinator = Person.objects.get(id=coord_id)
            university = University.objects.get(id=uni_id)
            sport = Sport.objects.get(id=sport_id)

            team = Team(coordinator=coordinator,
                        sport=sport, university=university, event=event)

            team.save()

            team_players = []
            for player_id in players:
                player = Person.objects.get(id=player_id)
                if player is not None:
                    team_player = PlayerTeam(player=player, team=team)
                    team_players.append(team_player)
                else:
                    team_players = []
                    team.delete()

            for team_player in team_players:
                team_player.save()

        redirect_url = reverse('team:team-home')
        return HttpResponseRedirect(redirect_url)


class TeamDeleteView(View):

    def post(self, request):
        team_id = request.POST.get('team')

        team = Team.objects.get(id=team_id)

        if team is not None:
            team.delete()

        redirect_url = reverse('team:team-home')
        return HttpResponseRedirect(redirect_url)
