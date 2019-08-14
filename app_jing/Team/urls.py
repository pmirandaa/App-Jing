from django.urls import path
from django.views.generic import TemplateView

from Team.views import TeamHome, TeamEditView, TeamDeleteView

app_name = 'team'

urlpatterns = [
    path('', TeamHome.as_view(), name='team-home'),
    path('create', TeamHome.as_view(), name='create-team'),
    path('edit', TeamEditView.as_view(), name='edit-team'),
    path('delete', TeamDeleteView.as_view(), name='delete-team')
]
