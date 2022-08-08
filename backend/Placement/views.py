from pprint import pprint
from rest_framework.viewsets import ModelViewSet

from django.db.models import Count
from django.db import connection

from rest_framework.decorators import action
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response

from .models import EventPlacement, SportPlacement
from .serializers import EventPlacementSerializer, SportPlacementSerializer, SportPlacementPointsSerializer
from .utils import sort_and_place
from Match.models import Match
from Sport.models import Sport, FinalSportPoints
from University.models import University
from Event.models import Event

from utils import is_valid_param


class EventPlacementViewSet(ModelViewSet):
    serializer_class = EventPlacementSerializer
    pagination_class = None
    queryset = EventPlacement.objects.all()

    def get_queryset(self):
        event = self.request.query_params.get('event')
        queryset = self.queryset
        if is_valid_param(event):
            queryset = queryset.filter(event=event)
        return queryset

    @action(detail=False, methods=['GET'], url_path='calculate/(?P<event_pk>\w+)')
    def calculate(self, request, event_pk):
        # Check if event is valid
        try:
            event_instance = Event.objects.get(pk=event_pk)
        except Event.DoesNotExist:
            raise NotFound("Event not found.")
        
        universities_qs = University.objects.filter(
            universityevent__event__exact=event_pk)

        # Get points assignation
        sport_points_qs = FinalSportPoints.objects.all()
        sport_points = {}
        for sp_item in sport_points_qs:
            if sport_points.get(sp_item.sport_type):
                sport_points[sp_item.sport_type][sp_item.place] = sp_item.points
            else:
                sport_points[sp_item.sport_type] = {sp_item.place:
                                                    sp_item.points}

        # Check if there are open sports
        sports_qs = Sport.objects.all()  # TODO filter by event
        # open_sports = [sp for sp in sports_qs if not sp.closed]
        # if len(open_sports) > 0:
        #     raise APIException(
        #         {"detail": "There are still open sports", "code": "open_sports", "open_sports": open_sports})

        sport_placements_qs = SportPlacement.objects.filter(
            sport__in=sports_qs).order_by('place').select_related('sport', 'university')  # TODO filter by event

        placements_by_sport = {sport.id: [] for sport in sports_qs}
        points_by_university = {univ.id: 0 for univ in universities_qs}
        for plcs in sport_placements_qs:
            this_sport_placement = SportPlacementPointsSerializer(
                plcs, excluded_fields=['id', 'sport'], context={'points_table': sport_points}
            ).data
            placements_by_sport.setdefault(
                plcs.sport_id, []).append(this_sport_placement)

            points_by_university[plcs.university_id] += this_sport_placement['points']

        event_placements = [{'event': event_pk, 'university': univ_id,
                             'points': pts} for univ_id, pts in points_by_university.items()]
        event_placements = sort_and_place(event_placements, key=['points', 'event'])

        event_placements_serializer = EventPlacementSerializer(
            data=event_placements, many=True)
        event_placements_serializer.is_valid()

        return Response({"event_placements": event_placements_serializer.data, "sport_placements": placements_by_sport})

    @action(detail=False, methods=['POST'])
    def set(self, request):
        event = request.data.get('event')
        placements = request.data.get('placements')
        if not is_valid_param(event) or not is_valid_param(placements):
            raise APIException(
                "You must give 'event' and 'placements' parameters")

        #event_instance = Event.objects.get(pk=event)
        # if event_instance.closed:
        #    raise APIException("Event is already closed")
        serializer = self.get_serializer(data=[{
            'event': event,
            'university': plc.get('university'),
            'points': plc.get('points'),
            'place': plc.get('place')}
            for plc in placements], many=True)
        serializer.is_valid(raise_exception=True)
        #event_instance.closed = True

        serializer.save()
        # event_instance.save()
        return Response(serializer.data)


class SportPlacementViewSet(ModelViewSet):
    serializer_class = SportPlacementSerializer
    pagination_class = None
    queryset = SportPlacement.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        sport = self.request.query_params.get('sport')
        if is_valid_param(sport):
            queryset = queryset.filter(sport=sport)
        return queryset

    @action(detail=False, methods=['GET'], url_path='calculate/(?P<sport_pk>[^/.]+)')
    def calculate(self, request, sport_pk):
        # Check if event is valid
        try:
            sport_instance = Sport.objects.get(pk=sport_pk)
        except Sport.DoesNotExist:
            raise NotFound("Sport not found.")
        event = request.query_params.get('event')
        # Check if sport and event are valid
        if not is_valid_param(event):
            raise APIException("You must give 'event' parameter")

        sport_instance = Sport.objects.get(pk=sport_pk)
        universities_qs = University.objects.filter(
            universityevent__event__exact=event)
        sport_points_qs = FinalSportPoints.objects.filter(
            sport_type=sport_instance.sport_type).values('place', 'points')
        sport_points = {sp_item['place']: sp_item['points']
                        for sp_item in sport_points_qs}

        # Get all wins by team for this sport and event
        winners_qs = Match.objects.filter(event=event, sport=sport_pk).values(
            'winner', 'winner__university').annotate(wins=Count('winner'))
        teams_wins = [{
            'team_id': w_item['winner'],
            'univ_id': w_item['winner__university'],
            'wins': w_item['wins']
        } for w_item in winners_qs]

        # Sum all wins grouped by university
        univ_wins = []
        for tw in teams_wins:
            # if tw['team_id'] is None: raise APIException("There are open matches for this sport")
            for uw in univ_wins:
                if uw['univ_id'] == tw['univ_id']:
                    uw['wins'] += tw['wins']
                    break
            else:
                if tw['team_id'] is not None:
                    univ_wins.append({
                        'univ_id': tw['univ_id'],
                        'wins': tw['wins'],
                        'participated': True,
                    })

        # Sort by wins and add placements
        univ_wins_sorted = sort_and_place(univ_wins, key='wins')

        # Add non-participant universities in last place
        for univ in universities_qs:
            for uw in univ_wins_sorted:
                if uw['univ_id'] == univ.pk:
                    break
            else:
                univ_wins_sorted.append({
                    'univ_id': univ.pk,
                    'wins': 0,
                    'participated': False,
                    'place': len(universities_qs),
                })

        serializer = self.get_serializer(data=[{
            'sport': sport_pk,
            'university': uw['univ_id'],
            'place': uw['place'],
            'participated': uw['participated']
        } for uw in univ_wins_sorted], many=True)
        serializer.is_valid(raise_exception=True)

        # Assign scores based on placement
        for uw in univ_wins_sorted:
            uw['score'] = sport_points[uw['place']]

        return Response(univ_wins_sorted)

    @action(detail=False, methods=['POST'])
    def set(self, request):
        event = request.data.get('event')
        sport = request.data.get('sport')
        placements = request.data.get('placements')
        if not is_valid_param(event) or not is_valid_param(sport) or not is_valid_param(placements):
            raise APIException(
                "You must give 'event', 'sport' and 'placements' parameters")

        sport_instance = Sport.objects.get(pk=sport)
        if sport_instance.closed:
            raise APIException("Sport is already closed")

        serializer = self.get_serializer(data=[{
            'sport': sport,
            'university': plc['university'],
            'place': plc['place'],
            'participated': plc['participated']
        } for plc in placements], many=True)
        serializer.is_valid(raise_exception=True)
        sport_instance.closed = True

        serializer.save()
        sport_instance.save()
        return Response(serializer.data)
