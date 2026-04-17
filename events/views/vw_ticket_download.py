from django.http import FileResponse
from django.views import View
from events.services.ticket_service import generate_ticket_pdf
from events.services.event_service import get_success_details


class TicketDownloadView(View):
    def get(self, request, booking_id):

        booking_data = get_success_details(booking_id)  # Details to Show in downloaded ticket

        file_path = generate_ticket_pdf(request, booking_data, booking_id)

        return FileResponse(open(file_path, 'rb'), as_attachment=True)