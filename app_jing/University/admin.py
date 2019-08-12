from django.contrib import admin

from University.models import University
from University.models import UniversityEvent


class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'short_name', 'overall_score')
    search_fields = ('name', 'city', 'short_name')


class UniversityEventAdmin(admin.ModelAdmin):
    list_display = ('event', 'university', 'is_host')
    search_fields = ('event', 'university', 'is_host')


admin.site.register(University, UniversityAdmin)
admin.site.register(UniversityEvent, UniversityEventAdmin)