from time import sleep
from rest_framework import viewsets
from utils.utils import is_valid_param
from .serializers import EventSerializer
from .models import Event


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    pagination_class = None
    queryset = Event.objects.all()

    def dispatch(self, request, *args, **kwargs):
        sleep(0.5)
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')
        year = self.request.query_params.get('year')
        current = self.request.query_params.get('current')
        if is_valid_param(name):
            queryset = queryset.filter(name__exact=name)
        if is_valid_param(year):
            queryset = queryset.filter(year__exact=year)
        if is_valid_param(current):
            queryset = queryset.filter(current__exact=current)
        queryset = queryset.order_by('year')
        return queryset
