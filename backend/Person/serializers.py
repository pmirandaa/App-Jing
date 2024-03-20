from rest_framework import serializers
from .models import Person, PER


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id',
                  'user',
                  'name',
                  'last_name',
                  'email',
                  'university',
                  'rut',
                  'phone_number',
                  'emergency_phone_number',
                  'pending_messages',
                  )
        
