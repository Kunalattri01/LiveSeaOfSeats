from django.views import View
from django.shortcuts import render
import requests
from django.conf import settings
from datetime import datetime


class TicketMasterEventsView(View):

    def get_best_image(self, images):
        for img in images:
            if img.get("ratio") == "3_2" and img.get("width", 0) >= 600:
                return img.get("url")
        return images[0].get("url") if images else None


    # ✅ SAME FORMAT as events_data
    def build_event(self, row):
        start = row.get("dates", {}).get("start", {})

        try:
            event_date = datetime.strptime(start.get("localDate"), "%Y-%m-%d").date() if start.get("localDate") else None
        except:
            event_date = None

        try:
            event_time = datetime.strptime(start.get("localTime"), "%H:%M:%S").time() if start.get("localTime") else None
        except:
            event_time = None

        attractions = row.get("_embedded", {}).get("attractions", [])

        if attractions and attractions[0].get("name"):
            name = attractions[0].get("name")
            unique_id = attractions[0].get("id")
        else:
            name = row.get("name")
            unique_id = row.get("id")

        return {
            "id": unique_id,
            "event_id": row.get("id"),
            "name": name,
            "image": self.get_best_image(row.get("images", [])),
            "date": event_date,
            "time": event_time,
            "city": row.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
            "url": row.get("url"),
        }


    # ✅ Fetch 1 event per keyword (hero)
    def fetch_hero_event(self, keyword):
        url = "https://app.ticketmaster.com/discovery/v2/events.json"

        params = {
            "apikey": settings.TICKETMASTER_API_KEY,
            "keyword": keyword,
            "size": 1,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
        except Exception:
            return None

        events = data.get('_embedded', {}).get('events', [])
        if not events:
            return None

        return self.build_event(events[0])


    def get(self, request):

        url = "https://app.ticketmaster.com/discovery/v2/events.json"

        params = {
            "apikey": settings.TICKETMASTER_API_KEY,
            "page": 0,
            "size": 20,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
        except Exception:
            data = {}

        raw_events = data.get('_embedded', {}).get('events', [])

        # 🔥 STEP 1: HERO EVENTS (WWE → BTS → Shakira)
        hero_events = []
        hero_ids = set()

        for keyword in ["wwe", "bts", "shakira"]:
            event = self.fetch_hero_event(keyword)
            if event:
                hero_events.append(event)
                hero_ids.add(event["id"])


        # 🔥 STEP 2: MAIN EVENTS (REMOVE HERO DUPLICATES)
        events_data = []
        unique_result = set()

        for row in raw_events:
            event = self.build_event(row)

            if event["id"] in unique_result:
                continue

            if event["id"] in hero_ids:   # ✅ avoid duplicates
                continue

            unique_result.add(event["id"])
            events_data.append(event)


        return render(request, 'ticketmaster/tm_events.html', {
            'events_data': events_data,
            'hero_events': hero_events,   # 🔥 use in carousel
            'TitleSearch': True,
            'ask_user_mail': True,
        })





# from django.views import View
# from django.shortcuts import render
# import requests
# from django.conf import settings
# from django.core.cache import cache
# from django.http import JsonResponse
# from datetime import datetime


# class TicketMasterEventsView(View):

#     def get_best_image(self, images):
#         for img in images:
#             if img.get("ratio") == "3_2" and img.get("width", 0) >= 600:
#                 return img.get("url")
#         return images[0].get("url") if images else None
    

#     def get(self, request):

#         # ALWAYS first page only
#         page = 0
#         url = "https://app.ticketmaster.com/discovery/v2/events.json"

#         city = request.session.get("city")
#         country = request.session.get("country")

#         params = {
#             "apikey": settings.TICKETMASTER_API_KEY,
#             "page": page,
#             "size": 20,
#             # "classificationName": "wwe",
#             # "countryCode": "US",
#         }

#         # if city:
#         #     params["city"] = city

#         # if country:
#         #     params["countryCode"] = country

#         try:
#             response = requests.get(url, params=params, timeout=10)
#             data = response.json()
#         except Exception:
#             data = {}

#         # return JsonResponse(data)
    
#         raw_events = data.get('_embedded', {}).get('events', [])

#         events_data = []
#         unique_result = set()

#         for row in raw_events:

#             attractions = row.get("_embedded", {}).get("attractions", [])

#             if attractions and attractions[0].get("name"):
#                 Name = attractions[0].get("name")
#                 Unique_id = attractions[0].get("id")
#             else:
#                 Name = row.get("name")
#                 Unique_id = row.get("id")

#             if Unique_id not in unique_result:
#                 unique_result.add(Unique_id)

#                 start = row.get("dates", {}).get("start", {})

#                 date_str = start.get("localDate")
#                 time_str = start.get("localTime")

#                 try:
#                     event_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
#                 except:
#                     event_date = None

#                 try:
#                     event_time = datetime.strptime(time_str, "%H:%M:%S").time() if time_str else None
#                 except:
#                     event_time = None
                    
#                 events_data.append({
#                     "id": Unique_id,
#                     "event_id": row.get("id"),
#                     "name": Name,
#                     "image": self.get_best_image(row.get("images", [])),
#                     "date": event_date,
#                     "time": event_time,
#                     "city": row.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
#                     "url": row.get("url"),
#                 })



#         return render(request, 'ticketmaster/tm_events.html', {
#             'events_data': events_data,
#             'TitleSearch' : True,
#             'ask_user_mail' : True,
#         })