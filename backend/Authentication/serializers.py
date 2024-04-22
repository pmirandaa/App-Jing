from rest_framework import serializers
from django.contrib.auth.models import User

from University.models import University
from Person.models import Person

class UserSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(many=False, queryset=Person.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username','email','person']
