from rest_framework import permissions
from Authentication.models import SportCoordinatorRole, EventCoordinatorRole, UniversityCoordinatorRole, TeamCoordinatorRole

class IsSportCoordinator(permissions.BasePermission):
    """
    Allows access only to coordinators for a given sport.
    """

    def has_permission(self, request):
        sport = request.data.get('sport')
        user = request.user
        try:
            role = SportCoordinatorRole.objects.get(person=user.id, sport=sport)
        except SportCoordinatorRole.DoesNotExist:
            return False
        return role.exists()

class IsEventCoordinator(permissions.BasePermission):
    """
    Allows access only to event coordinators.
    """

    def has_permission(self, request):
        event = request.data.get('event')
        user = request.user

        try:
            role = EventCoordinatorRole.objects.get(person=user.id, event=event).first()

        except EventCoordinatorRole.DoesNotExist:
            return False
        return role.exists()

class IsUniversityCoordinator(permissions.BasePermission):
    """
    Allows access only to university coordinators.
    """

    def has_permission(self, request):
        university = request.data.get('university')
        user = request.user
        
        try:
            role = UniversityCoordinatorRole.objects.get(person=user.id, university=university).first()
        
        except UniversityCoordinatorRole.DoesNotExist:
            return False
        
        return role.exists()

class IsTeamCoordinator(permissions.BasePermission):
    """
    Allows access only to team coordinators.
    """

    def has_permission(self, request):
        team = request.data.get('team')
        user = request.user
        
        try:
            role = TeamCoordinatorRole.objects.get(person=user.id, team=team).first()
        
        except TeamCoordinatorRole.DoesNotExist:
            return False
        return role.exists()

class AdminRole(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request):
        return request.user.is_superuser

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request):
        print('request.method: ' + request.method)
        return request.method in permissions.SAFE_METHODS