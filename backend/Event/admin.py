from django.contrib import admin

from Event.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    search_fields = ('name', 'year')


admin.site.register(Event, EventAdmin)
