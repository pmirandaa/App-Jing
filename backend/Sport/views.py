from time import sleep

from rest_framework import viewsets

from Sport.models import FinalSportPoints, Sport
from Sport.serializers import FinalSportPointsSerializer, SportSerializer


class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    pagination_class = None
    queryset = Sport.objects.all()

    def dispatch(self, request, *args, **kwargs):
        sleep(0.5)
        return super().dispatch(request, *args, **kwargs)


class FinalSportPointsViewSet(viewsets.ModelViewSet):
    serializer_class = FinalSportPointsSerializer
    queryset = FinalSportPoints.objects.all()
