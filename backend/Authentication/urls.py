from django.urls import path
from .views import UserViewSet, TokenObtainView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'Authentication'
urlpatterns = [
    path('register/', RegisterView.as_view({'get' : 'list'}), name='register'),
    path('token/', TokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]