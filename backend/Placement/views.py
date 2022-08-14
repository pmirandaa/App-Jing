from collections import defaultdict
from pprint import pprint
from rest_framework.viewsets import ModelViewSet

from django.db import connection
from django.db.models import Count, Case, When, Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.decorators import action
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response

from .models import EventPlacement, SportPlacement
from .serializers import EventPlacementSerializer, SportPlacementSerializer, SportPlacementPointsSerializer
from .utils import sort_and_place
from Match.models import Match, MatchTeam
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
            sport__in=sports_qs, event=event_pk).order_by('place').select_related('sport', 'university')

        placements_by_sport = {sport.id: [] for sport in sports_qs}
        points_by_university = {univ.id: 0 for univ in universities_qs}
        sport_placements_serializer = SportPlacementPointsSerializer(
            sport_placements_qs, excluded_fields=['id'], context={'points_table': sport_points}, many=True
        )
        for plcs in sport_placements_serializer.data:
            placements_by_sport.setdefault(
                plcs['sport'], []).append(plcs)

            points_by_university[plcs['university']] += plcs['points']

        ####################################################################
        # This code is replicated from SportPlacementViewSet.calculate
        # to calculate every sport that hasn't been calculated yet.
        # This forced calculation should only happen on explicit command,
        # and response should differentiate between sports that are closed
        # and have fixed standings and sports that haven't been calculated yet.
        # This should be refactored to a services module.
        calc_placements_by_sport = {}
        for sport in sports_qs:
            if placements_by_sport.get(sport.id):
                calc_placements_by_sport[sport.id] = placements_by_sport.get(
                    sport.id)
                continue
            # Get team statistics for this event and sport
            team_wins_qs = MatchTeam.objects.filter(match__event=event_pk, match__sport=sport.pk).values(
                'team', 'team__university'
            ).annotate(
                matches=Count('id'),
                wins=Count(Case(When(is_winner=True, then=1))),
                score=Sum('score'),
                attended=Count(Case(When(attended=True, then=1))))
            # Group statistics by university
            univ_wins_dict = {univ.pk:
                              {'matches': 0, 'wins': 0, 'score': 0,
                                  'attended': 0, 'participated': False}
                              for univ in universities_qs}
            for team_wins in team_wins_qs:
                this_univ = univ_wins_dict[team_wins['team__university']]
                this_univ['matches'] += team_wins['matches']
                this_univ['wins'] += team_wins['wins']
                this_univ['score'] += team_wins['score']
                this_univ['attended'] += team_wins['attended']
                this_univ['participated'] = this_univ['participated'] or bool(
                    team_wins['attended'])
            univ_wins_list = [{'university': univ, **univ_data}
                              for univ, univ_data in univ_wins_dict.items()]

            # Sort by statistics and add placements
            univ_wins_sorted = sort_and_place(
                univ_wins_list, key=['participated', 'wins', 'score'])

            # Add non-participant universities in last place
            for univ in universities_qs:
                for uw in univ_wins_sorted:
                    if uw['university'] == univ.pk:
                        break
                else:
                    univ_wins_sorted.append({
                        'university': univ.pk,
                        'wins': 0,
                        'participated': False,
                        'place': len(universities_qs),
                    })

            # TODO: Use serializer
            # serializer = SportPlacementSerializer(data=[{
            #     'sport': sport.pk,
            #     'event': event_pk,
            #     'university': uw['university'],
            #     'place': uw['place'],
            #     'participated': uw['participated']
            # } for uw in univ_wins_sorted], many=True)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()

            # Assign points based on placement
            for uw in univ_wins_sorted:
                uw['points'] = sport_points[sport.sport_type][uw['place']
                                                              ] if uw['participated'] else 0
                points_by_university[uw['university']] += uw['points']

            calc_placements_by_sport[sport.pk] = univ_wins_sorted

        placements_by_sport = calc_placements_by_sport
        ####################################################################

        event_placements = [{'event': event_pk, 'university': univ_id,
                             'points': pts} for univ_id, pts in points_by_university.items()]
        event_placements = sort_and_place(
            event_placements, key=['points', 'event'])

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
        # Check if sport is valid
        try:
            sport_instance = Sport.objects.get(pk=sport_pk)
        except Sport.DoesNotExist:
            raise NotFound("Sport not found.")

        # Check if event is valid
        event_pk = request.query_params.get('event')
        if not is_valid_param(event_pk):
            raise APIException("You must give 'event' parameter")
        try:
            event_instance = Event.objects.get(pk=event_pk)
        except Event.DoesNotExist:
            raise NotFound("Event not found.")

        # Get universities participating in this event
        universities_qs = University.objects.filter(
            universityevent__event=event_pk)

        # Get points assigned to each place for this sport
        sport_points_qs = FinalSportPoints.objects.filter(
            sport_type=sport_instance.sport_type).values('place', 'points')
        sport_points = {sp_item['place']: sp_item['points']
                        for sp_item in sport_points_qs}

        # Get open matches for this event and sport
        open_matches = Match.objects.filter(
            event=event_pk, sport=sport_pk, closed=False)

        # Get team statistics for this event and sport
        team_wins_qs = MatchTeam.objects.filter(match__event=event_pk, match__sport=sport_pk).values(
            'team', 'team__university'
        ).annotate(
            matches=Count('id'),
            wins=Count(Case(When(is_winner=True, then=1))),
            score=Sum('score'),
            attended=Count(Case(When(attended=True, then=1))))
        # Group statistics by university
        univ_wins_dict = {univ.pk:
                          {'matches': 0, 'wins': 0, 'score': 0,
                              'attended': 0, 'participated': False}
                          for univ in universities_qs}
        for team_wins in team_wins_qs:
            this_univ = univ_wins_dict[team_wins['team__university']]
            this_univ['matches'] += team_wins['matches']
            this_univ['wins'] += team_wins['wins']
            this_univ['score'] += team_wins['score']
            this_univ['attended'] += team_wins['attended']
            this_univ['participated'] = this_univ['participated'] or bool(
                team_wins['attended'])
        univ_wins_list = [{'university': univ, **univ_data}
                          for univ, univ_data in univ_wins_dict.items()]

        # Sort by statistics and add placements
        univ_wins_sorted = sort_and_place(
            univ_wins_list, key=['participated', 'wins', 'score'])

        # Add non-participant universities in last place
        for univ in universities_qs:
            for uw in univ_wins_sorted:
                if uw['university'] == univ.pk:
                    break
            else:
                univ_wins_sorted.append({
                    'university': univ.pk,
                    'wins': 0,
                    'participated': False,
                    'place': len(universities_qs),
                })

        # TODO: Use serializer
        serializer = self.get_serializer(data=[{
            'sport': sport_pk,
            'event': event_pk,
            'university': uw['university'],
            'place': uw['place'],
            'participated': uw['participated']
        } for uw in univ_wins_sorted], many=True)
        serializer.is_valid(raise_exception=True)
        # serializer.save()

        # Assign points based on placement
        for uw in univ_wins_sorted:
            uw['points'] = sport_points[uw['place']] if uw['participated'] else 0

        return Response({'open_matches': open_matches.count(), 'results': univ_wins_sorted})

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
