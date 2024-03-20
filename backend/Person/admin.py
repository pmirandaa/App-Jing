from django.contrib import admin

from Person.models import Person
from Person.models import PersonTemporaryCode
from Person.models import Role, PER


class PersonAdmin(admin.ModelAdmin):
    list_display = ('rut', 'Name', 'user', 'University')
    search_fields = ('rut', 'name', 'user__username', 'university__short_name')

    def University(self, obj):
        return obj.university.short_name or '-'

    def Name(self, obj):
        return f'{obj.name} {obj.last_name}'


class PersonTemporaryCodeAdmin(admin.ModelAdmin):
    list_display = ('date_expiration', 'person', 'code')
    search_fields = ('person__name',)

    def date_expiration(self, obj):
        return obj.expiration_date.strftime("%d/%m/%Y %H:%M")

    date_expiration.admin_order_field = 'timefield'

admin.site.register(Person, PersonAdmin)
admin.site.register(PersonTemporaryCode, PersonTemporaryCodeAdmin
)
admin.site.register(Role)
admin.site.register(PER)

