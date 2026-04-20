from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
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

        page = int(request.GET.get("page", 1)) - 1  # DRF → TM

        cache_key = f"tm_events_{page}"
        cached = cache.get(cache_key)

        if cached:
            return Response({
                "next": f"/api/events/?page={page + 2}" if len(cached) == 10 else None,
                "results": cached
            })

        url = "https://app.ticketmaster.com/discovery/v2/events.json"

        params = {
            "apikey": settings.TICKETMASTER_API_KEY,
            "classificationName": "music",
            "countryCode": "US",
            "size": 10,
            "page": page
        }

        response = requests.get(url, params=params)
        data = response.json()

        raw_events = data.get('_embedded', {}).get('events', [])

        events = []

        for row in raw_events:
            start = row.get("dates", {}).get("start", {})

            date_str = start.get("localDate")
            time_str = start.get("localTime")

            events.append({
                "id": row.get("id"),
                "name": row.get("name"),
                "image": self.get_best_image(row.get("images", [])),
                "date": datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None,
                "time": datetime.strptime(time_str, "%H:%M:%S").time() if time_str else None,
                "city": row.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
                "url": row.get("url"),
            })

        cache.set(cache_key, events, timeout=300)

        return Response({
            "next": f"/api/events/?page={page + 2}" if len(events) == 10 else None,
            "results": events
        })