from django.views import View
from django.shortcuts import render
from events.services.event_service import get_success_details


class PaymentSuccessView(View):
    def get(self, request, booking_id):

        booking_data = get_success_details(booking_id)

        context = {
            'TitleSearch' : True,
            'FooterSection' : True,
            "booking_data": booking_data,
            'booking_id' : booking_id,
        }

        return render(request, 'events/payment-success.html', context)