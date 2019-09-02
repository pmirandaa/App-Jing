from django.shortcuts import render
from django.views import View

from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

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
        players = Person.objects.exclude(is_admin=True)

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)

        return render(request, 'Team/baseTeam.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "teams": teams,
                          "sports": sports,
                          "universities": universities,
                          "players": players,
                          'alert': request.session.pop('alert', None)
                      })

    def post(self, request):
        uni_id = request.POST.get('university')
        sport_id = request.POST.get('sport')
        players = request.POST.getlist('player[]')
        captain_id = request.POST.get('captain')

        event = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)
                event = person.event

        num_players = len(players)
        if num_players > 0 and event is not None:

            coordinator = Person.objects.get(id=captain_id)
            university = University.objects.get(id=uni_id)
            sport = Sport.objects.get(id=sport_id)

            team = Team(coordinator=coordinator,
                        sport=sport, university=university, event=event)

            team_saved = False
            try:
                team.save()
                team_saved = True
            except:
                team.delete()

            if team_saved:

                team_players = []
                players_to_save = []
                for player_id in players:
                    player = Person.objects.get(id=player_id)
                    if player is not None:
                        player.is_player = True
                        players_to_save.append(player)
                        team_player = PlayerTeam(player=player, team=team)
                        team_players.append(team_player)
                    else:
                        players_to_save = []
                        team_players = []
                        team.delete()
                        request.session['alert'] = {
                            'type': 'danger',
                            'message': 'Ocurrió un error al crear el equipo'
                        }
                saved_data = []
                try:
                    for player in players_to_save:
                        player.save()
                        saved_data.append(player)

                    for team_player in team_players:
                        team_player.save()
                        saved_data.append(team_player)
                    request.session['alert'] = {
                        'type': 'success',
                        'message': 'Equipo creado con éxito'
                    }

                except:
                    for data in saved_data:
                        data.delete()
                        request.session['alert'] = {
                            'type': 'danger',
                            'message': 'Ocurrió un error al crear el equipo'
                        }
            else:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al crear el equipo'
                }

        redirect_url = reverse('team:team-home')
        return HttpResponseRedirect(redirect_url)


class TeamEditView(View):
    def get(self, request):
        team_id = request.GET.get('id')
        team = Team.objects.get(id=team_id)

        if team:
            players = Person.objects.filter(
                university=team.university).exclude(is_admin=True)
            tms = PlayerTeam.objects.filter(team=team)

            team_players = []
            for t_m in tms:
                team_players.append(t_m.player)

            return render(request, 'Team/editTeam.html',
                          {
                              "team": team,
                              "players": players,
                              "team_players": team_players
                          })

    def post(self, request):
        team_id = request.POST.get('id')
        uni_id = request.POST.get('university')
        sport_id = request.POST.get('sport')
        players = request.POST.getlist('player[]')
        captain_id = request.POST.get('edit-captain')

        event = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)
                event = person.event

        num_players = len(players)
        if num_players > 0 and event is not None:

            coordinator = Person.objects.get(id=captain_id)
            university = University.objects.get(id=uni_id)

            team = Team.objects.get(id=team_id)

            team_saved = False
            try:
                if coordinator.university == university:
                    team.coordinator = coordinator
                    team_saved = True
            except:
                pass

            tm_to_del = PlayerTeam.objects.filter(team=team)

            if team_saved:
                team_players = []
                players_to_save = []
                for player_id in players:
                    player = Person.objects.get(id=player_id)
                    if player is not None:
                        if player.university == university:
                            player.is_player = True
                            players_to_save.append(player)
                            team_player = PlayerTeam(player=player, team=team)
                            doer = Person.objects.get(user=request.user)
                            log = Log(
                                task = 'team_add_player',
                                value_before = str(team),
                                value_after = str(player),
                                person= f'{doer.name} {doer.last_name}',
                                date= timezone.now()
                            )
                            log.save()
                            team_players.append(team_player)
                        else:
                            request.session['alert'] = {
                                'type': 'danger',
                                'message': 'Ocurrió un error al crear el equipo'
                            }
                            team_players = []
                            players_to_save = []
                    else:
                        players_to_save = []
                        team_players = []
                        team.delete()
                        request.session['alert'] = {
                            'type': 'danger',
                            'message': 'Ocurrió un error al crear el equipo'
                        }

                saved_data = []
                try:
                    n_team_players = len(team_players)
                    n_players_to_save = len(players_to_save)
                    if n_team_players > 0 and n_players_to_save > 0:
                        for tm in tm_to_del:
                            tm.delete()

                        for player in players_to_save:
                            player.save()
                            saved_data.append(player)

                        for team_player in team_players:
                            team_player.save()
                            saved_data.append(team_player)

                        team.save()
                        request.session['alert'] = {
                            'type': 'success',
                            'message': 'Equipo creado con éxito'
                        }
                except:
                    for data in saved_data:
                        data.delete()
                        request.session['alert'] = {
                            'type': 'danger',
                            'message': 'Ocurrió un error al crear el equipo'
                        }
            else:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al crear el equipo'
                }

        redirect_url = reverse('team:team-home')
        return HttpResponseRedirect(redirect_url)


class TeamDeleteView(View):

    def post(self, request):
        team_id = request.POST.get('team')

        team = Team.objects.get(id=team_id)

        if team is not None:
            try:
                doer = Person.objects.get(user=request.user)
                log = Log(
                    task = 'team_deleted',
                    value_before = str(team),
                    value_after = 'None',
                    person= f'{doer.name} {doer.last_name}',
                    date= timezone.now()
                )
                log.save()
                team.delete()
                request.session['alert'] = {
                    'type': 'info',
                    'message': 'Equipo eliminado con exito'
                }
            except:
                request.session['alert'] = {
                    'type': 'danger',
                    'message': 'Ocurrió un error al eliminar el equipo'
                }

        redirect_url = reverse('team:team-home')
        return HttpResponseRedirect(redirect_url)
