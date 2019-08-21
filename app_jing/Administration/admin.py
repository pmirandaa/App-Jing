from django.contrib import admin

from Administration.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display=('task', 'person', 'date')
    search_fields=('task', 'person', 'date')


admin.site.register(Log, LogAdmin)
