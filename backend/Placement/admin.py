from django.contrib import admin

from .models import EventPlacement, SportPlacement

class EventPlacementAdmin(admin.ModelAdmin):
    pass

class SportPlacementAdmin(admin.ModelAdmin):
    pass

admin.site.register(EventPlacement, EventPlacementAdmin)
admin.site.register(SportPlacement, SportPlacementAdmin)