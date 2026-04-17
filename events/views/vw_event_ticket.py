from django.views import View
from django.shortcuts import render, redirect
from events.services.event_service import get_event_details, get_ticket_category
from booking.services.booking_service import create_temp_booking
from django.http import HttpResponse

class EventTicketView(View):
    def get(self, request, show_id):

        event_details = get_event_details(show_id) # get selected event details
        tickets_details = get_ticket_category(show_id) # get tickets category and related detail
    
        context = {
            'TitleSearch' : True,
            'FooterSection' : True,
            'event_details' : event_details,
            'tickets_details' : tickets_details,
            'show_id' : show_id
        }

        return render(request, 'events/event-ticket.html', context)
    
    
    
    def post(self, request, *args, **kwargs):

        show_id = kwargs.get('show_id')

        ticket_id = request.POST.get('ticket_id')
        qty = int(request.POST.get('qty'))

        items = [
            {"ticket_type_id": ticket_id, "qty": qty}
        ]

        try:
            temp_booking = create_temp_booking(user=request.user, show_id=show_id, items=items)
        except Exception as e:
            return HttpResponse(str(e))

        return redirect('TicketOptionsPage', show_id=show_id, temp_booking_id=temp_booking.id)