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
    
    def get(self, request, attraction_id):

        print('attr', attraction_id)

        url = "https://app.ticketmaster.com/discovery/v2/events.json"

        params = {
            "apikey": settings.TICKETMASTER_API_KEY,
            "attractionId": attraction_id,
            "size": 50,
            "sort": "date,asc"
        }

        response = requests.get(url, params=params)
        data = response.json()

        raw_data = data.get("_embedded", {}).get("events", [])
        # return JsonResponse(raw_data, safe=False)
        venue_list = []
        hero_event = None

        for i, row in enumerate(raw_data):

            start = row.get("dates", {}).get("start", {})
            venue = row.get("_embedded", {}).get("venues", [{}])[0]

            try:
                event_date = datetime.strptime(start.get("localDate"), "%Y-%m-%d").date()
            except:
                event_date = None

            try:
                event_time = datetime.strptime(start.get("localTime"), "%H:%M:%S").time()
            except:
                event_time = None

            event_data = {
                "event_name": row.get("name"),
                "date": event_date,
                "time": event_time,
                "address": venue.get("name"),
                "city": venue.get("city", {}).get("name"),
                "ticket_url": row.get("url"),
            }

            venue_list.append(event_data)

            # first event = hero section
            if i == 0:
                hero_event = {
                    # "name": row.get("name"),
                    "name": raw_data[0].get("_embedded", {}).get("attractions", [{}])[0].get("name"),
                    "image": self.get_best_image(row.get("images", [])),
                    "city": venue.get("city", {}).get("name"),
                    "pleaseNote": raw_data[0].get("pleaseNote"),
                    "country": venue.get("country", {}).get("name"),
                    "ticket_url": row.get("url"),
                }

        return render(request, "ticketmaster/tm_event_details.html", {
            "event": hero_event,
            "venue": venue_list,
            'TitleSearch' : True,
            'ask_user_mail' : True,
        })

    # def get(self, request, attraction_id):
        
    #     url = "https://app.ticketmaster.com/discovery/v2/events.json"

    #     params = {
    #         "apikey": settings.TICKETMASTER_API_KEY,
    #         "attractionId": attraction_id,
    #         "size": 50,   # get more matches
    #         "sort": "date,asc"
    #     }

    #     response = requests.get(url, params=params)
    #     data = response.json()

    #     raw_data = data.get("_embedded", {}).get("events", [{}])

    #     # return JsonResponse(raw_data, safe=False)


    #     events_data = []

    #     for row in raw_data:

    #         events_data.append({
    #             'image': self.get_best_image(data.get("images", [])),
    #         })

    #         events_data['venus_list'] = [{
    #             'event_name' : row['name']
    #         }]

    #     # # return JsonResponse(venue, safe=False)
        
    #     # # ---- SAFE EXTRACTION ----
    #     # attractions = data.get("_embedded", {}).get("attractions", [])

    #     # event = {
    #     #     "id": data.get("id"),
    #     #     "name": data.get("name"),
    #     #     "date": datetime.strptime(data.get("dates", {}).get("start", {}).get("localDate"), '%Y-%m-%d').date(),
    #     #     "time": datetime.strptime(data.get("dates", {}).get("start", {}).get("localTime"), '%H:%M:%S').time(),
    #     #     "status": data.get("dates", {}).get("status", {}).get("code"),
    #     #     "category": data.get("classifications", [{}])[0].get("segment", {}).get("name"),
    #     #     "genre": data.get("classifications", [{}])[0].get("genre", {}).get("name"),
    #     #     "latitude": venue.get("location", {}).get("latitude"),
    #     #     "longitude": venue.get("location", {}).get("longitude"),
    #     #     "venue_name": venue.get("name"),
    #     #     "city": venue.get("city", {}).get("name"),
    #     #     "country": venue.get("country", {}).get("name"),
    #     #     "address": venue.get("address", {}).get("line1"),
    #     #     "description": data.get("info") or data.get("pleaseNote"),
    #     #     "image": self.get_best_image(data.get("images", [])),
    #     #     "gallery": [img.get("url") for img in data.get("images", [])[:3]],
    #     #     "price_min": None,
    #     #     "price_max": None,
    #     #     "ticket_url": data.get("url"),

    #     #     "venue_extra": {
    #     #         "phone": venue.get("boxOfficeInfo", {}).get("phoneNumberDetail"),
    #     #         "open_hours": venue.get("boxOfficeInfo", {}).get("openHoursDetail"),
    #     #         "payment": venue.get("boxOfficeInfo", {}).get("acceptedPaymentDetail"),

    #     #         "parking": venue.get("parkingDetail"),
    #     #         "accessibility": venue.get("accessibleSeatingDetail"),

    #     #         "rules": venue.get("generalInfo", {}).get("generalRule"),
    #     #         "child_rule": venue.get("generalInfo", {}).get("childRule"),
    #     #     },

    #     #     "performers": [
    #     #         {
    #     #             "name": artist.get("name"),
    #     #             "image": artist.get("images", [{}])[0].get("url")
    #     #         }
    #     #         for artist in attractions
    #     #     ]
    #     # }

    #     # if data.get("priceRanges"):
    #     #     event["price_min"] = data["priceRanges"][0].get("min")
    #     #     event["price_max"] = data["priceRanges"][0].get("max")


    #     # similar_events = []

    #     # try:
    #     #     similar_url = "https://app.ticketmaster.com/discovery/v2/events.json"

    #     #     similar_params = {
    #     #         "apikey": settings.TICKETMASTER_API_KEY,
    #     #         "city": venue.get("city", {}).get("name"),
    #     #         "classificationName": event["category"],
    #     #         "size": 6
    #     #     }

    #     #     sim_res = requests.get(similar_url, params=similar_params)
    #     #     sim_data = sim_res.json()

    #     #     for ev in sim_data.get("_embedded", {}).get("events", []):
    #     #         if ev.get("id") == attraction_id:
    #     #             continue

    #     #         v = ev.get("_embedded", {}).get("venues", [{}])[0]

    #     #         similar_events.append({
    #     #             "id": ev.get("id"),
    #     #             "name": ev.get("name"),
    #     #             "image": self.get_best_image(ev.get("images", [])),
    #     #             "venue": v.get("name"),
    #     #             "city": v.get("city", {}).get("name"),
    #     #         })

    #     #     similar_events = similar_events[:5]

    #     # except Exception as e:
    #     #     print("Similar events error:", e)

    #     context = {
    #         'TitleSearch' : True,
    #         'ask_user_mail' : True,
    #         # 'event' : event,
    #         # 'similar_events' : similar_events,
    #         'events_data' : events_data,
    #     }

    #     return render(request, "ticketmaster/tm_event_details.html", context)