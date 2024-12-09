from rest_framework import serializers
from .models import Person, PER, Role
from Event.serializers import EventSerializer
from Event.models import Event

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
                  'roles')

class PERSerializer(serializers.ModelSerializer):
    #person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), many=True)
    #event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all().values('name'), many=True)
    #role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all().values('roles'), many=True)

    class Meta:
        model = PER
        fields = (
                  'event',
                  'role')
                  
class PersonSerializer(serializers.ModelSerializer):
    roles =   PERSerializer(many=True, read_only=True)
    class Meta:
        model = Person
        fields = ['id',
                  'user',
                  'name',
                  'last_name',
                  'email',
                  'university',
                  'rut',
                  'phone_number',
                  'emergency_phone_number',
                  'pending_messages',
                  'roles'
        ]


