from django.urls import path
from .views import *


urlpatterns = [
    path('reportfirst/', ReportFirstView.as_view(), name='ReportFirstPage'),
    path('events_status/', EventsStatusView.as_view(), name='EventsStatusPage'),
    path('edit_event/', EditEventView.as_view(), name='EditEventPage'),
]