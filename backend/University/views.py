from rest_framework import viewsets
from .serializers import UniversitySerializer
from .models import University


class UniversityViewSet(viewsets.ModelViewSet):
    serializer_class = UniversitySerializer
    queryset = University.objects.all()
