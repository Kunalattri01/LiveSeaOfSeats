from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.core.cache import cache
from datetime import datetime
import requests


class TicketMasterAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def get_best_image(self, images):
        for img in images:
            if img.get("ratio") == "3_2" and img.get("width", 0) >= 600:
                return img.get("url")
        return images[0].get("url") if images else None

    def get(self, request):

        page = int(request.GET.get("page", 1)) - 1

        cache_key = f"tm_events_{page}"
        cached = cache.get(cache_key)

        # If cached, return directly (no pagination logic here)
        if cached:
            return Response({
                "next": f"/api/events/?page={page + 2}",  # simple fallback
                "results": cached
            })

        url = "https://app.ticketmaster.com/discovery/v2/events.json"

        params = {
            "apikey": settings.TICKETMASTER_API_KEY,
            # "classificationName": "wwe",
            "page": page,
            "size": 20,  # increase size (important)
            "sort": "name,asc"  # stabilize results
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
        except Exception:
            data = {}

        raw_events = data.get('_embedded', {}).get('events', [])

        events_data = []
        unique_result = set()

        for row in raw_events:

            attractions = row.get("_embedded", {}).get("attractions", [])

            if attractions and attractions[0].get("name"):
                Name = attractions[0].get("name")
                Unique_id = attractions[0].get("id")
            else:
                Name = row.get("name")
                Unique_id = row.get("id")

            if Unique_id in unique_result:
                continue

            unique_result.add(Unique_id)

            start = row.get("dates", {}).get("start", {})

            date_str = start.get("localDate")
            time_str = start.get("localTime")

            try:
                event_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
            except:
                event_date = None

            try:
                event_time = datetime.strptime(time_str, "%H:%M:%S").time() if time_str else None
            except:
                event_time = None

            events_data.append({
                "id": Unique_id,
                "event_id": row.get("id"),
                "name": Name,
                "image": self.get_best_image(row.get("images", [])),
                "date": event_date,
                "time": event_time,
                "city": row.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
                "url": row.get("url"),
            })

        # CORRECT pagination logic
        page_info = data.get("page", {})
        total_pages = page_info.get("totalPages", 0)

        next_page = None
        if page + 1 < total_pages:
            next_page = f"/api/events/?page={page + 2}"

        # cache only results
        cache.set(cache_key, events_data, timeout=300)

        return Response({
            "next": next_page,
            "results": events_data
        })