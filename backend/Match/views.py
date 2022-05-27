from django.utils import timezone
from django.shortcuts import render
from django.views import View

from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.db import connection

from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Person.models import Person
from Team.models import Team
from Match.models import Match
from .serializers import MatchInfoSerializer, MatchTeamSerializer, MatchCreateSerializer, MatchUpdateSerializer
from Administration.models import Log


class MatchViewSet(ModelViewSet):
    read_serializer_class = MatchInfoSerializer
    create_serializer_class = MatchCreateSerializer
    update_serializer_class = MatchUpdateSerializer
    queryset = Match.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            serializer_class = self.create_serializer_class
        elif self.action in ['update', 'partial_update']:
            serializer_class = self.update_serializer_class
        else:
            serializer_class = self.read_serializer_class
        return serializer_class

    @action(detail=False, queryset=queryset.exclude(state=Match.PLAYED))
    def pending(self, request):
        """
        Get all Matches that are NOT marked as played.
        """
        return self.list(request)

    @action(detail=False, queryset=queryset.filter(state=Match.PLAYED))
    def played(self, request):
        """
        Get all Matches that are marked as played.
        """
        return self.list(request)

    @action(methods=['POST'], detail=True)
    def finish(self, request):
        pass

    # def create(self, request):
    #     create_serializer = self.get_serializer(data=request.data)
    #     create_serializer.is_valid(raise_exception=True)
    #     match_instance = create_serializer.save()
    #     read_serializer = self.read_serializer_class(match_instance)
    #     return Response(read_serializer.data, status=status.HTTP_304_NOT_MODIFIED)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     update_serializer = self.get_serializer(
    #         instance, data=request.data, partial=partial)
    #     update_serializer.is_valid(raise_exception=True)
    #     match_instance = update_serializer.save()

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}

    #     read_serializer = self.get_serializer(match_instance)
    #     return Response(read_serializer.data)


class MatchStartView(View):
    def post(self, request):
        match_id = request.POST.get('match')

        match = Match.objects.get(id=match_id)

        if match is not None:
            doer = Person.objects.get(user=request.user)
            log = Log(
                task='started_match',
                value_before=match.state,
                value_after=Match.PLAYING,
                person=f'{doer.name} {doer.last_name}',
                date=timezone.now()
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
                task='finished_match',
                value_before=match.state,
                value_after=Match.PLAYED,
                person=f'{doer.name} {doer.last_name}',
                date=timezone.now()
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
                task='closed_match',
                value_before=match.closed,
                value_after='True',
                person=f'{doer.name} {doer.last_name}',
                date=timezone.now()
            )
            log.save()
            match.state = Match.PLAYED
            match.closed = True
            winner = Team.objects.get(id=winner_id)
            match.winner = winner
            match.save()

        redirect_url = reverse('match:matches-section')
        return HttpResponseRedirect(redirect_url)


class MatchCommentView(View):

    def post(self, request):
        match_id = request.POST.get('match')
        team_id = request.POST.get('team')
        comment = request.POST.get('comment')

        match = Match.objects.get(pk=match_id)
        match_team = match.teams.get(pk=team_id)

        doer = Person.objects.get(user=request.user)
        log = Log(
            task='match_add_comment',
            value_before='None',
            value_after=comment,
            person=f'{doer.name} {doer.last_name}',
            date=timezone.now()
        )
        log.save()

        match_team.comment = comment
        match_team.save()

        return HttpResponseRedirect(reverse('match:matches-section'))
