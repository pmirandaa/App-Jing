from rest_framework import serializers

from Sport.serializers import SportSerializer
from University.serializers import UniversitySerializer
from Person.serializers import PersonSerializer
from .models import Team, PlayerTeam


class TeamSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    university = UniversitySerializer(read_only=True)
    coordinator = PersonSerializer(read_only=True)
    class Meta:
        model = Team
        fields = ('__all__')

class PlayerTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerTeam
        fields = ('__all__')
