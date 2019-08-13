from django.contrib import admin

from Sport.models import Sport
from Sport.models import FinalSportPoints


class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'sport_type', 'coordinator')
    search_fields = ('name', 'gender', 'sport_type', 'coordinator__name')


class FinalSportPointsAdmin(admin.ModelAdmin):
    list_display = ('sport_type', 'place', 'points')
    search_fields = ('sport_type', 'place', 'points')


admin.site.register(Sport, SportAdmin)
admin.site.register(FinalSportPoints, FinalSportPointsAdmin)