from time import sleep

from rest_framework import viewsets

from Sport.models import  Sport, FinalSportPoints
from Sport.serializers import SportSerializer, FinalSportPointsSerializer
from utils import bool_param, is_valid_param

class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    pagination_class = None
    queryset = Sport.objects.all()

    def dispatch(self, request, *args, **kwargs):
        sleep(0.5)
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        event = self.request.query_params.get('event')
        queryset = self.queryset
        if is_valid_param(event):
            queryset = queryset.filter(eventsport__event=event)
        return queryset


class FinalSportPointsViewSet(viewsets.ModelViewSet):
     serializer_class = FinalSportPointsSerializer
     queryset = FinalSportPoints.objects.all()
