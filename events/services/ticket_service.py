from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
import os

def generate_ticket_pdf(request, booking_data, booking_id):

    folder = os.path.join(settings.MEDIA_ROOT, "tickets")
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"ticket_{booking_id}.pdf")

    if os.path.exists(file_path):
        return file_path

    html_string = render_to_string(
        'pdf/event_ticket.html',
        {
            'booking_data': booking_data,
            'request': request
        }
    )

    HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    ).write_pdf(file_path)

    return file_path