from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import UserSerializer, TokenObtain, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from Person.serializers import Person
from Person.serializers import PersonSerializer



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
    person = None
    permissions = None
    if request.user.is_authenticated:
        if Person.objects.filter(user=request.user).exists():
                person = PersonSerializer(Person.objects.get(user=request.user))
                permissions = request.user.get_all_permissions()

    data = {
        "permissions" : permissions,
    }

    return Response(data)
