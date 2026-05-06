import json
from django.views import View
from django.http import JsonResponse

class SetCityView(View):

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        request.session['city'] = data.get("city")
        request.session['country'] = data.get("country")
        request.session['country_code'] = (data.get("country_code") or "").upper()
        request.session['lat'] = data.get("lat")
        request.session['lng'] = data.get("lng")

        request.session.modified = True

        return JsonResponse({
            "status": "success"
        })