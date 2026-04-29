import json
from django.http import JsonResponse
from django.views import View


class SetCityView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        request.session['city'] = data.get("city")
        request.session['country'] = data.get("country")
        request.session['lat'] = data.get("lat")
        request.session['lng'] = data.get("lng")

        return JsonResponse({"status": "success"})