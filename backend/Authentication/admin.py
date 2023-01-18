from django.contrib import admin
from .models import AdminRole, EventCoordinatorRole, UniversityCoordinatorRole, SportCoordinatorRole, TeamCoordinatorRole

admin.site.register(AdminRole)
admin.site.register(EventCoordinatorRole)
admin.site.register(UniversityCoordinatorRole)
admin.site.register(SportCoordinatorRole)
admin.site.register(TeamCoordinatorRole)
