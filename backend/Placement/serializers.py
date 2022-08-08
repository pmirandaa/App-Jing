from rest_framework import serializers

from serializers import DynamicFieldsModelSerializer

from .models import EventPlacement, SportPlacement
from Sport.models import FinalSportPoints
from Sport.serializers import SportSerializer
from University.serializers import UniversitySerializer

class EventPlacementSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = EventPlacement
        fields = ('__all__')

class SportPlacementSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SportPlacement
        fields = ('__all__')

class SportPlacementPointsSerializer(SportPlacementSerializer):
    points = serializers.SerializerMethodField("get_points")

    def get_points(self, obj):
        points = 0
        points_table = self.context.get('points_table')
        if points_table is None:
            try:
                points_qs = FinalSportPoints.objects.get(sport_type=obj.sport.sport_type, place=obj.place)
                points = points_qs.points
            except FinalSportPoints.DoesNotExist:
                pass
        else:
            try:
                points = points_table[obj.sport.sport_type][obj.place]
            except KeyError:
                pass
        
        return points