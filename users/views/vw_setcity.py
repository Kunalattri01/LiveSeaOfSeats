import json
from django.http import JsonResponse
from django.views import View


class SetCityView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        city = data.get("city")
        country = data.get("country")

        request.session['city'] = city
        request.session['country'] = country

        return JsonResponse({"status": "success"})