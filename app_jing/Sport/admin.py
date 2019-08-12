from django.contrib import admin

from Sport.models import Sport


class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'sport_type', 'coordinator')
    search_fields = ('name', 'gender', 'sport_type', 'coordinator__name')

admin.site.register(Sport, SportAdmin)
