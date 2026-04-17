from django.urls import path
from .views import *
from .views.vw_payment import create_order, verify_payment

urlpatterns = [
    path('', EventView.as_view(), name='EventPage'),
    path('event_details/<int:event_id>/', EventDetailsView.as_view(), name='EventDetailsPage'),
    path('event_speaker/<int:event_id>/<int:speaker_id>/', EventSpealerView.as_view(), name='EventSpeakerPage'),
    path('event_ticket/<int:show_id>/', EventTicketView.as_view(), name='EventTicketPage'),
    path('event_checkout/<int:show_id>/<int:temp_booking_id>/', EventCheckoutView.as_view(), name='EventCheckoutPage'),
    path('ticket_options/<int:show_id>/<int:temp_booking_id>/', TicketOptionsView.as_view(), name='TicketOptionsPage'),
    path('event_timing/<int:event_id>/', EventTimingView.as_view(), name='EventTimingPage'),
    path('payment_success/<int:booking_id>/', PaymentSuccessView.as_view(), name='PaymentSuccessPage'),
    path('download-ticket/<int:booking_id>/', TicketDownloadView.as_view(), name='TicketDownloadPage'),

    path('create-order/', create_order, name='create_order'),
    path('verify-payment/', verify_payment, name='verify_payment'),

]