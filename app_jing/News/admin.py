from django.contrib import admin

from News.models import NewsCategory
from News.models import News


class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'color')
    search_fields = ('event', 'name', 'color')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('publication_date', 'title', 'publisher', 'category')
    search_fields = ('title', 'publisher__name', 'category__name')

    def publication_date(self, obj):
        return obj.date.strftime("%d/%m/%Y %H:%M")

    publication_date.admin_order_field = 'timefield'

admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(News, NewsAdmin)
