from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import UserSerializer, TokenObtain, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from Person.serializers import Person
from Person.serializers import PersonSerializer
from Placement import permissions



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class TokenObtainView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtain

class RegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

@api_view(['GET'])
def get_permissions(request):
    user_permissions = {}
    if request.user.is_authenticated:
        if Person.objects.filter(user=request.user).exists():
                user_permissions['isSportCoordinator'] = permissions.IsSportCoordinator().has_permission(request)
                user_permissions['isEventCoordinator'] = permissions.IsEventCoordinator().has_permission(request)
                user_permissions['isUniversityCoordinator'] = permissions.IsUniversityCoordinator().has_permission(request)
                user_permissions['isTeamCoordinator'] = permissions.IsTeamCoordinator().has_permission(request)
                user_permissions['admin'] = permissions.AdminRole().has_permission(request)

    data = {
        "permissions" : user_permissions,
    }

    return Response(data)
