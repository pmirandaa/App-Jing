from rest_framework import serializers
from .models import Team, PlayerTeam


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('__all__')

class PlayerTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerTeam
        fields = ('__all__')
