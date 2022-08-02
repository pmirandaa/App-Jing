from time import sleep
from rest_framework import viewsets
from .serializers import EventSerializer
from .models import Event


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    pagination_class = None
    queryset = Event.objects.all()

    def dispatch(self, request, *args, **kwargs):
        sleep(0.5)
        return super().dispatch(request, *args, **kwargs)
