import json
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from events.services.event_service import get_event_ticket_summary
from booking.models import TempBooking
from booking.services.booking_service import confirm_booking


def create_order(request):
    if request.method != 'POST':
        return JsonResponse({ 'error' : 'Invalid Request' }, status = 400)
    
    data = json.loads(request.body)
    
    temp_booking_id = data.get("temp_booking_id")

    if not temp_booking_id:
        return JsonResponse({"error": "Missing booking id"}, status=400)
    

    summary = get_event_ticket_summary(temp_booking_id)
    total_amount = summary[0]['TotalTicketPrice']


    amount = int(total_amount * 100) # Convert to paise

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return JsonResponse({
        "order_id": order["id"],
        "amount": amount,
        "key": settings.RAZORPAY_KEY_ID
    })


@csrf_exempt
def verify_payment(request):
    if request.method != "POST":
        return JsonResponse({"status": "failed"}, status=400)
    
    data = json.loads(request.body)


    order_id = data.get("razorpay_order_id")
    payment_id = data.get("razorpay_payment_id")
    signature = data.get("razorpay_signature")

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    # try:
        # ⚠️ TEMP: skip verification for testing
    client.utility.verify_payment_signature({
        "razorpay_order_id": order_id,
        "razorpay_payment_id": payment_id,
        "razorpay_signature": signature
    })

    temp_booking_id = data.get("temp_booking_id")
    print('temp_booking_id : ', temp_booking_id)

    if not temp_booking_id:
        return JsonResponse({"status": "failed"})

    temp_booking = TempBooking.objects.get(id=temp_booking_id)

    booking =  confirm_booking(request, temp_booking, payment_success=True, payment_id=payment_id, order_id=order_id)

    return JsonResponse({"status": "success", "booking_id": booking.id})

    # except Exception as e:
    #     print("Payment verification failed:", str(e))
    #     return JsonResponse({"status": "failed"})