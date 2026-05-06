from django.urls import path
from .views import *
from .drf_api import *


urlpatterns = [
    path('', TicketMasterEventsPageView.as_view(), name='TicketMasterEventsPage'),
    path('api/events/', TicketMasterAPINewView.as_view(), name='TicketMasterAPINew'),
    path('event_details/<str:attraction_id>/', TicketMasterEventDetailsView.as_view(), name="TicketMasterEventDetailsPage"),
    path('save_lead/', save_lead, name='save_lead'),
    # path('', TicketMasterEventsView.as_view(), name='TicketMasterEventsPage'),
    # path('api/events/', TicketMasterAPIView.as_view(), name='TicketMasterAPI'),
    # path('event_details/<str:attraction_id>/', TicketMasterEventDetailsView.as_view(), name="TicketMasterEventDetailsPage"),
]