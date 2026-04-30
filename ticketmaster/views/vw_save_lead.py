from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from users.models import EventLead

@csrf_exempt
def save_lead(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        EventLead.objects.create(
            name=name,
            email=email,
            phone=phone
        )

        request.session['lead_saved'] = True
        request.session['user_name'] = name

        return JsonResponse({"status": "success"})