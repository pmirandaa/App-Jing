from datetime import datetime
from time import sleep
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Count

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.utils import is_valid_param, bool_param

from Location.models import Location
from Match.models import Match
from Sport.models import Sport
from University.models import University
from .exceptions import MatchAlreadyPlayed, MatchAlreadyClosed, MatchNotPlayed
from .serializers import MatchInfoSerializer, MatchStatusSerializer, MatchCreateSerializer, MatchUpdateSerializer
from Administration.models import Log


class MatchViewSet(ModelViewSet):
    read_serializer_class = MatchInfoSerializer
    create_serializer_class = MatchCreateSerializer
    update_serializer_class = MatchUpdateSerializer
    status_serializer_class = MatchStatusSerializer
    queryset = Match.objects.all()

    def dispatch(self, request, *args, **kwargs):
        sleep(0.5)
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
