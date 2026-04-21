from django.views import View
from django.shortcuts import render
from django.conf import settings
import requests
from datetime import datetime
from django.http import JsonResponse

class TicketMasterEventDetailsView(View):

    def get_best_image(self, images):
        for img in images:
            if img.get("ratio") == "16_9" and img.get("width", 0) > 800:
                return img.get("url")
        return images[0].get("url") if images else None


    def get(self, request, event_id):
        
        url = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}.json"

        params = {
            "apikey": settings.TICKETMASTER_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        # return JsonResponse(data)
        
        # ---- SAFE EXTRACTION ----
        venue = data.get("_embedded", {}).get("venues", [{}])[0]
        attractions = data.get("_embedded", {}).get("attractions", [])

        event = {
            "id": data.get("id"),
            "name": data.get("name"),
            "date": datetime.strptime(data.get("dates", {}).get("start", {}).get("localDate"), '%Y-%m-%d').date(),
            "time": datetime.strptime(data.get("dates", {}).get("start", {}).get("localTime"), '%H:%M:%S').time(),
            "status": data.get("dates", {}).get("status", {}).get("code"),
            "category": data.get("classifications", [{}])[0].get("segment", {}).get("name"),
            "genre": data.get("classifications", [{}])[0].get("genre", {}).get("name"),
            "latitude": venue.get("location", {}).get("latitude"),
            "longitude": venue.get("location", {}).get("longitude"),
            "venue_name": venue.get("name"),
            "city": venue.get("city", {}).get("name"),
            "country": venue.get("country", {}).get("name"),
            "address": venue.get("address", {}).get("line1"),
            "description": data.get("info") or data.get("pleaseNote"),
            "image": self.get_best_image(data.get("images", [])),
            "gallery": [img.get("url") for img in data.get("images", [])[:3]],
            "price_min": None,
            "price_max": None,
            "ticket_url": data.get("url"),

            "venue_extra": {
                "phone": venue.get("boxOfficeInfo", {}).get("phoneNumberDetail"),
                "open_hours": venue.get("boxOfficeInfo", {}).get("openHoursDetail"),
                "payment": venue.get("boxOfficeInfo", {}).get("acceptedPaymentDetail"),

                "parking": venue.get("parkingDetail"),
                "accessibility": venue.get("accessibleSeatingDetail"),

                "rules": venue.get("generalInfo", {}).get("generalRule"),
                "child_rule": venue.get("generalInfo", {}).get("childRule"),
            },

            "performers": [
                {
                    "name": artist.get("name"),
                    "image": artist.get("images", [{}])[0].get("url")
                }
                for artist in attractions
            ]
        }

        if data.get("priceRanges"):
            event["price_min"] = data["priceRanges"][0].get("min")
            event["price_max"] = data["priceRanges"][0].get("max")


        similar_events = []

        try:
            similar_url = "https://app.ticketmaster.com/discovery/v2/events.json"

            similar_params = {
                "apikey": settings.TICKETMASTER_API_KEY,
                "city": venue.get("city", {}).get("name"),
                "classificationName": event["category"],
                "size": 6
            }

            sim_res = requests.get(similar_url, params=similar_params)
            sim_data = sim_res.json()

            for ev in sim_data.get("_embedded", {}).get("events", []):
                if ev.get("id") == event_id:
                    continue

                v = ev.get("_embedded", {}).get("venues", [{}])[0]

                similar_events.append({
                    "id": ev.get("id"),
                    "name": ev.get("name"),
                    "image": self.get_best_image(ev.get("images", [])),
                    "venue": v.get("name"),
                    "city": v.get("city", {}).get("name"),
                })

            similar_events = similar_events[:5]

        except Exception as e:
            print("Similar events error:", e)

        context = {
            'TitleSearch' : True,
            'ask_user_mail' : True,
            'event' : event,
            'similar_events' : similar_events,
        }

        return render(request, "ticketmaster/tm_event_details.html", context)