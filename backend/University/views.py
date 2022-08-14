from time import sleep
from rest_framework import viewsets
from .serializers import UniversitySerializer
from .models import University

from utils import is_valid_param


class UniversityViewSet(viewsets.ModelViewSet):
    serializer_class = UniversitySerializer
    pagination_class = None
    queryset = University.objects.all()

    def dispatch(self, request, *args, **kwargs):
        sleep(0.5)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        event = self.request.query_params.get('event')
        queryset = self.queryset
        if is_valid_param(event):
            queryset = queryset.filter(universityevent__event=event)
        return queryset
