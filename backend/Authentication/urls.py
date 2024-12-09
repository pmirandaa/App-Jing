from django.urls import path
from django.views.generic import TemplateView
from .import views

app_name = 'Authentication'

urlpatterns = [
    path("login/", views.login_view, name="api_login"),
    path("logout/", views.logout_view, name="api_logout"),
    path("session/", views.session_view, name="api_session"),
    path("whoami/", views.whoami_view, name="api_whoami"),
    path("signin/", views.signin_view, name="api_signin"),
    path("dataload/", views.DataLoadView, name="api_dataload"),
    path("persondataload/", views.PersonDataLoadView, name="api_persondataload"),
    path("excel/", views.sendExcel, name="api_excel"),
    path("createteam/", views.CreateTeam, name="api_createteam"),
    path("createperson/", views.CreatePerson, name="api_createperson")

]