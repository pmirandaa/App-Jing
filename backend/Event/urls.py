from django.urls import path
from django.views.generic import TemplateView

from Event.views import EventHome, EventEditView, EventDeleteView

app_name = 'Event'

urlpatterns = [
    path('', EventHome.as_view(), name='event-home'),
    path('create', EventHome.as_view(), name='create-event'),
    path('edit', EventEditView.as_view(), name='edit-event'),
    path('delete', EventDeleteView.as_view(), name='delete-event')]