from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id',
                  'user',
                  'event',
                  'name',
                  'last_name',
                  'email',
                  'university',
                  'rut',
                  'phone_number',
                  'emergency_phone_number',
                  'is_admin',
                  'is_organizer',
                  'is_university_coordinator',
                  'is_sports_coordinator',
                  'is_player',
                  'is_coach',
                  'has_avatar',
                  'pending_messages',
                  )
