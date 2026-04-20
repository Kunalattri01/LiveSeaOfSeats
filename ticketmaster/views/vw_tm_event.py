from django.views import View
from django.shortcuts import render
import requests
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from datetime import datetime


class TicketMasterEventsView(View):

    def get_best_image(self, images):
        for img in images:
            if img.get("ratio") == "3_2" and img.get("width", 0) >= 600:
                return img.get("url")
        return images[0].get("url") if images else None
    

    def get(self, request):

        # ALWAYS first page only
        page = 0

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

        events_data = []

        for row in raw_events:
            start = row.get("dates", {}).get("start", {})

            date_str = start.get("localDate")
            time_str = start.get("localTime")

            events_data.append({
                "id": row.get("id"),
                "name": row.get("name"),
                "image": self.get_best_image(row.get("images", [])),
                "date": datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None,
                "time": datetime.strptime(time_str, "%H:%M:%S").time() if time_str else None,
                "city": row.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
                "url": row.get("url"),
            })

        return render(request, 'ticketmaster/tm_events.html', {
            'events_data': events_data,
            'ask_user_mail' : True
        })
    


















# class TicketMasterEventsView(View):

#     def get_best_image(self, images):
#         for img in images:
#             if img.get("ratio") == "3_2" and img.get("width", 0) >= 600:
#                 return img.get("url")
#         return images[0].get("url") if images else None
    

#     def get(self, request):

#         page = int(request.GET.get("page", 0))

#         cache_key = f"ticketmaster_events_{page}"
#         cached_events = cache.get(cache_key)

#         if cached_events:
#             if request.headers.get("x-requested-with") == "XMLHttpRequest":
#                 return JsonResponse({"events": cached_events})
#             return render(request, 'ticketmaster/tm_events.html', {
#                 'events_data': cached_events
#             })

#         url = "https://app.ticketmaster.com/discovery/v2/events.json"

#         params = {
#             "apikey": settings.TICKETMASTER_API_KEY,
#             "classificationName": "music",
#             "countryCode": "US",
#             "size": 10
# 
# ,
#             "page": page
#         }

#         try:
#             response = requests.get(url, params=params, timeout=10)
#             data = response.json()
#         except Exception as e:
#             print("API Error:", e)
#             data = {}

#         raw_events = data.get('_embedded', {}).get('events', [])

#         events_data = []

#         for row in raw_events:
#             start = row.get("dates", {}).get("start", {})

#             events_data.append({
#                 "id": row.get("id"),
#                 "name": row.get("name"),
#                 "image": self.get_best_image(row.get("images", [])),
#                 "date": start.get("localDate"),
#                 "time": start.get("localTime"),
#                 "city": row.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
#                 "url": row.get("url"),
#             })

#         cache.set(cache_key, events_data, timeout=300)

#         if request.headers.get("x-requested-with") == "XMLHttpRequest":
#             return JsonResponse({"events": events_data})

#         return render(request, 'ticketmaster/tm_events.html', {
#             'events_data': events_data
#         })















































# from django.views import View
# from django.shortcuts import render
# from django.conf import settings
# from datetime import datetime
# import requests
# from django.core.cache import cache


# class TicketMasterEventsView(View):

#     # ONLY this helper added (image selection)
#     def get_best_image(self, images):
#         for img in images:
#             if img.get("ratio") == "3_2" and img.get("width", 0) >= 600:
#                 return img.get("url")
#         return images[0].get("url") if images else None
    


#     def get(self, request):

#         cached_events = cache.get("ticketmaster_events")

#         if cached_events:
#             return render(request, 'ticketmaster/tm_events.html', {
#                 'FooterSection': True,
#                 'events_data': cached_events
#             })

#         url = "https://app.ticketmaster.com/discovery/v2/events.json"

#         params = {
#             "apikey": settings.TICKETMASTER_API_KEY,
#             "classificationName": "music",
#             "countryCode": "US",
#             "size": 10


#         }

#         try:
#             response = requests.get(url, params=params, timeout=10)
#             data = response.json()
#         except Exception:
#             data = {}

#         raw_events = data.get('_embedded', {}).get('events', [])

#         events_data = []

#         for row in raw_events:

#             start_str = row.get("dates", {}).get("start", {})

#             date_str = start_str.get("localDate")
#             time_str = start_str.get("localTime")

#             events_data.append({
#                 "id": row.get("id"),
#                 "name": row.get("name"),
#                 "image": self.get_best_image(row.get("images", [])),
#                 "date": datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None,
#                 "time": datetime.strptime(time_str, "%H:%M:%S").time() if time_str else None,
#                 "venue": row.get("_embedded", {}).get("venues", [{}])[0].get("name"),
#                 "city": row.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
#                 "category": row.get("classifications", [{}])[0].get("segment", {}).get("name"),
#                 "url": row.get("url"),
#             })

#         cache.set("ticketmaster_events", events_data, timeout=300)

#         context = {
#             'FooterSection': True,
#             'events_data': events_data
#         }

#         return render(request, 'ticketmaster/tm_events.html', context)