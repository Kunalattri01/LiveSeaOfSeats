import json
from django.http import JsonResponse
from django.views import View

class SetCityView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        city = data.get("city")

        request.session['city'] = city

        return JsonResponse({"status": "success"})