from django.views import View
from django.shortcuts import render
from events.services.event_service import get_ticket_rcv_mode, get_event_ticket_summary

class EventCheckoutView(View):
    def get(self, request, show_id, temp_booking_id):

        ticket_options = get_ticket_rcv_mode(show_id) # Get Ticket Receving Mode ( M-Ticket, Email, Box-Office etc. )
        booking_summary = get_event_ticket_summary(temp_booking_id) # Get Ticket Summary ( Total Ticket Booked, ShowTiming, Tickets Count etc. )

        context = {
           'TitleSearch' : True,
            'FooterSection' : True,
            'ticket_options' : ticket_options,
            'booking_summary' : booking_summary,
            'show_id' : show_id,
            'temp_booking_id' : temp_booking_id,
        }

        return render(request, 'events/event-checkout.html', context)