from rest_framework import serializers

from Sport.serializers import SportSerializer
from University.serializers import UniversitySerializer
from Person.serializers import PersonSerializer
from Sport.models import Sport
from University.models import University
from .models import Team, PlayerTeam


class TeamSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    university = UniversitySerializer(read_only=True)
    coordinator = PersonSerializer(read_only=True)
    sport_name = serializers.CharField(source='sport.name', read_only=True)
    class Meta:
        model = Team
        fields = ('__all__')

class PlayerTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerTeam
        fields = ('__all__')

class TeamTestSerializer(serializers.ModelSerializer):
    #sport = serializers.PrimaryKeyRelatedField(queryset=Sport.objects.all())
    #university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())
    #sport_name = serializers.CharField(source='sport.name', read_only=True)
    class Meta:
        model = Team
        fields = ('__all__')