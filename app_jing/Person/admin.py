from django.contrib import admin

from Person.models import Person
from Person.models import PersonAvatar
from Person.models import PersonTemporaryCode

admin.site.register(Person)
admin.site.register(PersonAvatar)
admin.site.register(PersonTemporaryCode)
