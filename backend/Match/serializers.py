from multiprocessing import Event
from django.db import connection
from django.forms import ValidationError
from pkg_resources import require
from rest_framework import serializers

from Location.serializers import LocationSerializer
from Team.models import Team

from .models import Match, MatchTeam


# MatchTeam serializers
# -----------------

class MatchTeamSerializer(serializers.ModelSerializer):
    """
    Base serializer for MatchTeam model.
    """
    match_team_id = serializers.IntegerField(source='id', read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team')

    class Meta:
        model = MatchTeam
        fields = ('match_team_id', 'team_id', 'match', 'score', 'comment')


class MatchTeamInfoSerializer(MatchTeamSerializer):
    """
    Includes detailed information about participating teams.
    """
    team_university_short_name = serializers.CharField(
        source='team.university.short_name', read_only=True)

    class Meta(MatchTeamSerializer.Meta):
        fields = ('match_team_id', 'team_id', 'score',
                  'comment', 'team_university_short_name')


class MatchTeamCreateSerializer(MatchTeamSerializer):
    class Meta(MatchTeamSerializer.Meta):
        fields = ('match_team_id', 'team_id', 'score', 'comment')


class MatchTeamUpdateSerializer(MatchTeamSerializer):
    """
    Serializer for updating MatchTeam.
    Overrides default read_only property for id AutoField.
    """
    match_team_id = serializers.IntegerField(source='id', read_only=False)

    class Meta(MatchTeamSerializer.Meta):
        fields = ('match_team_id', 'team_id', 'score', 'comment')


class MatchTeamStatusSerializer(MatchTeamSerializer):
    class Meta(MatchTeamSerializer.Meta):
        fields = ('match_team_id', 'team_id', 'score', 'comment')


# Match serializers
# -----------------

class MatchSerializer(serializers.ModelSerializer):
    """
    Base serializer for Match model.
    """
    class Meta:
        model = Match
        fields = ('id', 'location', 'event', 'length', 'date', 'teams',
                  'state', 'sport', 'closed', 'time_closed', 'winner')

    def updateMatchTeams(self, match_instance, match_teams_data):
        """
        Update MatchTeam relations.
        If a MatchTeam ID is given, that instance will be updated,
        otherwise it will try to match by team
        """
        for mt_data in match_teams_data:
            mt_id = mt_data.pop('id', None)
            mt_team = mt_data.get('team', None)
            print("data:",mt_data)
            print("ids:",mt_id, mt_team)
            if mt_id:
                mt_instance = match_instance.match_teams.filter(id=mt_id)
            else:
                print("match_teams:",match_instance.match_teams)
                mt_instance = match_instance.match_teams.filter(
                    team=mt_team)
            print("instance:",mt_instance)
            if mt_instance is not None:
                mt_instance.update(**mt_data)


class MatchInfoSerializer(MatchSerializer):
    """
    Maps foreign keys to their corresponding serializers to convey further
    details on a single query.
    """
    location = LocationSerializer(read_only=True)
    # event = EventSerializer(read_only=True)
    # sport = SportSerializer(read_only=True)
    teams = MatchTeamInfoSerializer(
        many=True, read_only=True, source='match_teams')


class MatchStatusSerializer(MatchSerializer):
    """
    """
    teams = MatchTeamStatusSerializer(
        many=True, source='match_teams', required=False)

    class Meta(MatchSerializer.Meta):
        fields = ('id', 'teams', 'state', 'closed', 'time_closed', 'winner')

    def update(self, instance, validated_data):
        print(validated_data)
        match_teams = validated_data.pop('match_teams', [])
        # Update directly editable attributes
        if validated_data:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        self.updateMatchTeams(instance, match_teams)
        return instance


class MatchCreateSerializer(MatchSerializer):
    """
    Automatically creates corresponding MatchTeams just having the teams IDs.
    """
    teams = MatchTeamCreateSerializer(many=True, source='match_teams')

    class Meta(MatchSerializer.Meta):
        read_only_fields = ['closed', 'time_closed', 'state', 'winner']

    def validate_teams(self, value):
        """
        Check that there are at least 2 participating teams.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "There must be at least 2 participating teams")
        return value

    def create(self, validated_data):
        """
        Creates a new Match, then creates a new MatchTeam for each
        participating team, associated with created Match.
        If MatchTeam creation fails, deletes newly created Match.
        """
        match_teams = validated_data.pop('match_teams')
        match = Match.objects.create(**validated_data)

        for match_team_data in match_teams:
            match_team_data['match'] = match
            MatchTeam.objects.create(**match_team_data)

        return match


class MatchUpdateSerializer(MatchSerializer):
    teams = MatchTeamUpdateSerializer(many=True, source='match_teams')

    class Meta(MatchSerializer.Meta):
        read_only_fields = ['closed', 'time_closed', 'state', 'winner']

    def update(self, instance, validated_data):
        match_teams = validated_data.pop('match_teams', [])  
        # Update directly editable attributes
        if validated_data:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

        self.updateMatchTeams(instance, match_teams)
        return instance
