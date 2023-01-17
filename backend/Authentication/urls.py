from django.urls import path
from .views import UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView

app_name = 'Authentication'
urlpatterns = [
    path('register/', UserViewSet.as_view({'get' : 'list'}), name='register'),
    path('refresh/', TokenRefreshView.as_view()),
    path('', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]