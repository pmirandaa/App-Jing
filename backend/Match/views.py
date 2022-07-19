from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from django.views import View

from django.http.response import HttpResponseRedirect
from django.urls import reverse

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Person.models import Person
from Team.models import Team
from Match.models import Match
from .exceptions import AlreadyFinished, AlreadyClosed, AlreadyStarted
from .serializers import MatchInfoSerializer, MatchStatusSerializer, MatchCreateSerializer, MatchUpdateSerializer
from Administration.models import Log


class MatchViewSet(ModelViewSet):
    read_serializer_class = MatchInfoSerializer
    create_serializer_class = MatchCreateSerializer
    update_serializer_class = MatchUpdateSerializer
    status_serializer_class = MatchStatusSerializer
    queryset = Match.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        event = self.request.query_params.get('event')
        my_matches = self.request.query_params.get('my_matches')
        participants = self.request.query_params.get('participants')
        state = self.request.query_params.get('state')
        sport = self.request.query_params.get('sport')
        location = self.request.query_params.get('location')
        if event is not None:
            queryset = queryset.filter(event__exact=event)
        if my_matches is not None:
            user = self.request.user
            queryset = queryset.filter(match_teams__team__playerteam__player__exact=user.id)
        if participants is not None:
            participants_list = participants.split(',')
            queryset = queryset.filter(match_teams__team__university__in=participants_list)
        if state is not None:
            queryset = queryset.filter(state__exact=state)
        if sport is not None:
            queryset = queryset.filter(sport__exact=sport)
        if location is not None:
            queryset = queryset.filter(location__exact=location)
        return queryset

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

    @action(detail=True, methods=['POST'])
    def start(self, request, pk):
        match = self.get_object()
        if match.closed:
            raise AlreadyClosed()
        elif match.state == 'MIF' or match.time_closed:
            raise AlreadyFinished()
        elif match.state == 'MIC':
            raise AlreadyStarted()
        elif match.state == 'MTB':
            data = {'state': 'MIC'}
            serializer = self.status_serializer_class(
                match, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['POST'])
    def finish(self, request, pk):
        match = self.get_object()
        if match.closed:
            raise AlreadyClosed()
        elif match.state == 'MIF' or match.time_closed:
            raise AlreadyFinished()
        elif match.state in ['MTB', 'MIC']:
            data = {'state': 'MIF', 'time_closed': datetime.now()}
            data = {**data, **request.data}
            serializer = self.status_serializer_class(
                match, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['POST'])
    def close(self, request, pk):
        match = self.get_object()
        if match.closed:
            raise AlreadyClosed()
        data = {'state': 'MIF', 'closed': True}
        if not match.time_closed:
            data['time_closed'] = datetime.now()
        data = {**data, **request.data}
        serializer = self.status_serializer_class(
            match, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # def create(self, request):
    #     create_serializer = self.get_serializer(data=request.data)
    #     create_serializer.is_valid(raise_exception=True)
    #     match_instance = create_serializer.save()
    #     read_serializer = self.read_serializer_class(match_instance)
    #     return Response(read_serializer.data, status=status.HTTP_201_CREATED)

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

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

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
