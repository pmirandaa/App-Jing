from rest_framework import viewsets
from .serializers import EventSerializer
from .models import Event


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
