from rest_framework import serializers
from .models import News, NewsCategory


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('__all__')

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('__all__')