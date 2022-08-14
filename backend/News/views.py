from rest_framework import viewsets

from News.models import NewsCategory
from News.models import News
from News.serializers import NewsSerializer
from News.serializers import NewsCategorySerializer


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()


class NewsCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = NewsCategorySerializer
    queryset = NewsCategory.objects.all()
