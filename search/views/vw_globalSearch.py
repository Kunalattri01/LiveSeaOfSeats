from django.http import JsonResponse
from django.views import View
from search.services.search_event_db import global_suggestions


class SearchSuggestionView(View):

    def get(self, request):
        
        q = request.GET.get("q", "").strip()
        types = request.GET.get("type", "")
        city = request.GET.get("city")
        date = request.GET.get("date")

        types_list = types.split(",") if types else []

        results = global_suggestions(q, types_list, city, date)

        return JsonResponse({"results": results})