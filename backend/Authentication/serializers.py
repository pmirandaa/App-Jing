from rest_framework import serializers
from django.contrib.auth.models import User

from University.models import University


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
