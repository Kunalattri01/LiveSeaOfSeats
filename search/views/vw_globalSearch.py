from django.http import JsonResponse
from django.views import View
from search.services.search_event_db import global_suggestions


class SearchSuggestionView(View):
    def get(self, request):
        q = request.GET.get("q", "").strip()
        results = global_suggestions(q)
        return JsonResponse({"results": results})