from django.contrib import admin

from Administration.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display=('task', 'person', 'date', 'value_before', 'value_after')
    search_fields=('task', 'person', 'date')


admin.site.register(Log, LogAdmin)
