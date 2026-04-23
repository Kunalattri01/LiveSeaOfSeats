from django.urls import path
from .views import *
from .drf_api import *


urlpatterns = [
    path('', TicketMasterEventsView.as_view(), name='TicketMasterEventsPage'),
    path('api/events/', TicketMasterAPIView.as_view(), name='TicketMasterAPI'),
    path('event_details/<str:attraction_id>/', TicketMasterEventDetailsView.as_view(), name="TicketMasterEventDetailsPage"),
]