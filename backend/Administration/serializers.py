from rest_framework import serializers

from University.serializers import UniversitySerializer
from .models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log

class AdminSerializer(serializers.Serializer):
    name = serializers.CharField()
    # people = None
    # events = None
    universities = UniversitySerializer(many=True)
    # locations = None
    # person = None
    # sports = None
    # sport_types = None
    # genders = None
    # sports_coords = None
    # unis_coords = None
    # alert = request.session.pop('alert', None)