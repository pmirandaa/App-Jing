from rest_framework import serializers
from .models import Sport , FinalSportPoints


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('__all__')

class FinalSportPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalSportPoints
        fields = ('__all__')