import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from events.services.ticket_service import generate_ticket_pdf
from events.services.event_service import get_success_details
from events.services.whatsapp_service import send_whatsapp_message


# EMAIL SENDER (existing logic)
def send_ticket_email(user_email, booking_data, pdf_path):

    html_content = render_to_string(
        'mail_templates/event_ticket_mail.html',
        {'booking_data': booking_data}
    )

    email = EmailMessage(
        subject="Your Ticket Booking 🎟",
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )

    email.content_subtype = "html"
    email.attach_file(pdf_path)
    email.send()


# # WORKER FUNCTION (runs in background)
# def process_ticket_email_worker(request, booking):
#     try:
#         booking_data = get_success_details(booking.id)

#         pdf_path = generate_ticket_pdf(request, booking_data, booking.id)

#         send_ticket_email(
#             # booking.user.email,
#             'kunalnana77@gmail.com',
#             booking_data,
#             pdf_path
#         )

#     except Exception as e:
#         print("Email Thread Error:", str(e))


def process_ticket_email_worker(request, booking):
    try:
        booking_data = get_success_details(booking.id)

        pdf_path = generate_ticket_pdf(request, booking_data, booking.id)

        # ✅ EMAIL
        send_ticket_email(
            'kunalnana77@gmail.com',  # replace later with booking.user.email
            booking_data,
            pdf_path
        )

        # ✅ WHATSAPP (ADD THIS PART)

        # generate ticket URL
        ticket_url = request.build_absolute_uri(
            f"/download-ticket/{booking.id}/"
        )

        message = f"""
        *Booking Confirmation*

        Your tickets have been successfully booked.

        *Event:* {booking.event.title}
        *Schedule:* {booking.showtime.show_date}, {booking.showtime.start_time}
        *Venue:* {booking.event.venue}

        *Booking ID:* {booking.order_id}

        *Tickets:*
        """

        for item in booking.bookingitem_set.all():
            message += f"\n• {item.category.name} ({item.ticket_id})"

        message += f"""

        *Access your ticket:*
        {ticket_url}

        Please present the QR code at entry. Arrive 15 minutes prior to the event.
        """

        send_whatsapp_message(
            '+919958066256',
            # booking.user.phone,   # make sure this field exists
            message
        )

        print("Email + WhatsApp sent successfully")

    except Exception as e:
        print("Worker Error:", str(e))


# ASYNC FUNCTION (thread starter)
def process_ticket_email_async(request, booking):

    thread = threading.Thread(
        target=process_ticket_email_worker,
        args=(request, booking)
    )

    thread.daemon = True   # important
    thread.start()













# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.conf import settings

# def send_ticket_email(user_email, booking_data, pdf_path):

#     html_content = render_to_string(
#         'mail_templates/event_ticket_mail.html',
#         {'booking_data': booking_data}
#     )

#     email = EmailMessage(
#         subject="Your Ticket Booking 🎟",
#         body=html_content,
#         from_email=settings.EMAIL_HOST_USER,
#         to=[user_email],
#     )

#     email.content_subtype = "html"

#     email.attach_file(pdf_path)
#     email.send()