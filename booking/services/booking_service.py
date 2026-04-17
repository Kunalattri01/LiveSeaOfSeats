from django.db import transaction
from django.db.models import F
from django.utils.timezone import now
from datetime import timedelta
import uuid
import qrcode
from io import BytesIO
from django.core.signing import Signer
from django.core.files import File
from booking.models import ShowTime, TempBooking, TempBookingItem, Booking, BookingItem, TicketType
from events.services.email_service import process_ticket_email_async


# ---------------------- [ vw_event_ticket ] ----------------------
def create_temp_booking(user, show_id, items):
    """
        items = [
            {"ticket_type_id": 1, "qty": 2},
            {"ticket_type_id": 2, "qty": 1}
        ]
    """

    with transaction.atomic():

        show = ShowTime.objects.get(id=show_id)

        temp_booking = TempBooking.objects.create(
            user=user,
            event=show.event,
            showtime=show,
            expires_at=now() + timedelta(minutes=5),
            status="ACTIVE")

        for item in items:
            tt_id = item["ticket_type_id"]
            qty = item["qty"]

            updated = TicketType.objects.filter(
                id=tt_id,
                quantity__gte=F('sold') + F('locked') + qty
            ).update(
                locked=F('locked') + qty
            )

            if updated == 0:
                raise Exception("Tickets not available")
            
            ticket_type = TicketType.objects.get(id=tt_id)
            
            TempBookingItem.objects.create(
                temp_booking=temp_booking,
                ticket_type=ticket_type,
                quantity=qty
            )

    return temp_booking





# CONFIRM BOOKING (PAYMENT SUCCESS)
def confirm_booking(request, temp_booking, payment_success=True, payment_id=None, order_id=None):

    if temp_booking.status != "ACTIVE":
        raise Exception("Booking already processed")

    if not payment_success:
        release_lock(temp_booking)
        raise Exception("Payment failed")

    with transaction.atomic():

        items = TempBookingItem.objects.select_related('ticket_type').filter(
            temp_booking=temp_booking
        )

        total_amount = sum([
            item.quantity * item.ticket_type.price
            for item in items
        ])

        # Create Booking
        booking = Booking.objects.create(
            user=temp_booking.user,
            event=temp_booking.event,
            showtime=temp_booking.showtime,
            total_amount=total_amount,
            status="CONFIRMED",
            payment_id=payment_id,
            order_id=order_id
        )

        # Generate secure token
        booking.qr_token = uuid.uuid4().hex
        booking.save(update_fields=["qr_token"])

        # Generate QR
        generate_booking_qr(booking)

        # Process items
        for item in items:

            TicketType.objects.filter(id=item.ticket_type_id).update(
                locked=F('locked') - item.quantity,
                sold=F('sold') + item.quantity
            )

            for _ in range(item.quantity):
                ticket_id = f"TKT-{uuid.uuid4().hex[:8]}"

                BookingItem.objects.create(
                    booking=booking,
                    category=item.ticket_type,
                    quantity=1,
                    price=item.ticket_type.price,
                    ticket_id=ticket_id
                )

        # Mark temp booking consumed
        temp_booking.status = "CONSUMED"
        temp_booking.save(update_fields=["status"])

    
    # OUTSIDE TRANSACTION (VERY IMPORTANT)
    # booking_data = get_success_details(booking.id)
        
    # pdf_path = generate_ticket_pdf(request, booking_data, booking.id)

    # send_ticket_email(
    #     request.user.email,
    #     booking,
    #     pdf_path
    # )


    process_ticket_email_async(request, booking)

    return booking





# GENERATE QR FOR THE TICKET BOOKED
def generate_booking_qr(booking):

    signer = Signer()
    qr_data = signer.sign(booking.qr_token)

    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format='PNG')

    buffer.seek(0)

    file_name = f"booking_{booking.id}.png"

    booking.qr_code.save(file_name, File(buffer), save=True)






#  RELEASE LOCK (FAIL / CANCEL / EXPIRE)
def release_lock(temp_booking):

    if temp_booking.status != "ACTIVE":
        return

    with transaction.atomic():

        items = TempBookingItem.objects.select_related('ticket_type').filter(
            temp_booking=temp_booking
        )

        for item in items:
            TicketType.objects.filter(
                id=item.ticket_type_id,
                locked__gte=item.quantity
            ).update(
                locked=F('locked') - item.quantity
            )

        temp_booking.status = "EXPIRED"
        temp_booking.save(update_fields=["status"])


# AUTO EXPIRE FUNCTION (USE IN CRON / COMMAND)
def expire_temp_bookings():

    expired = TempBooking.objects.filter(
        expires_at__lt=now(),
        status="ACTIVE"
    )

    for tb in expired:
        release_lock(tb)