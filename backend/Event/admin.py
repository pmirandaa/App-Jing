from django.contrib import admin

from Event.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'current')
    search_fields = ('name', 'year', 'current')


admin.site.register(Event, EventAdmin)
