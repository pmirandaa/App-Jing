from rest_framework import serializers
from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    #person = serializers.StringRelatedField(many=True)
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    class Meta:
        model = Message
        fields = ('id','sender_name','chat','subject','body','is_read','date','deleted')

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('__all__')
