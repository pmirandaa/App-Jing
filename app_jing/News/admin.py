from django.contrib import admin

from News.models import NewsCategory
from News.models import News


admin.site.register(NewsCategory)
admin.site.register(News)
