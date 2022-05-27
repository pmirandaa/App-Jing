from django.contrib import admin

from Location.models import Location


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'university')
    search_fields = ('name', 'university__short_name', 'university__name')


admin.site.register(Location, LocationAdmin)
