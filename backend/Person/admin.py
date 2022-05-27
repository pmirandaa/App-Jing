from django.contrib import admin

from Person.models import Person
from Person.models import PersonAvatar
from Person.models import PersonTemporaryCode


class PersonAdmin(admin.ModelAdmin):
    list_display = ('rut', 'Name', 'user', 'University', 'role')
    search_fields = ('rut', 'name', 'user__username', 'university__short_name')

    def role(self, obj):
        if obj.is_admin:
            return 'Admin'
        elif obj.is_organizer:
            return 'Organizador'
        elif obj.is_university_coordinator:
            return 'Coordinador Universidad'
        elif obj.is_sports_coordinator:
            return 'Coordinador Deporte'
        elif obj.is_player:
            return 'Jugador'
        elif obj.is_coach:
            return 'Capitan/Entrenador'

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
admin.site.register(PersonAvatar)
admin.site.register(PersonTemporaryCode, PersonTemporaryCodeAdmin
)
