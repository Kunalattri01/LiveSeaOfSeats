import requests
from django.conf import settings
from django.urls import reverse

def tm_search(query, size=5, city=None, date=None):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    params = {
        "apikey": settings.TICKETMASTER_API_KEY,
        "keyword": query,
        "size": size,
    }

    if city:
        params["city"] = city

    if date:
        params["startDateTime"] = f"{date}T00:00:00Z"

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except Exception:
        return []

    events = data.get("_embedded", {}).get("events", [])

    results = []
    unique_result = set()

    for e in events:
        attractions = e.get("_embedded", {}).get("attractions", [])

        if attractions and attractions[0].get("name"):
            name = attractions[0].get("name")
            unique_id = attractions[0].get("id")
        else:
            name = e.get("name")
            unique_id = e.get("id")

        if unique_id in unique_result:
            continue
        unique_result.add(unique_id)

        venue_data = e.get("_embedded", {}).get("venues", [{}])[0]

        results.append({
            "id": unique_id,
            "title": name,
            "type": "events",
            "city": venue_data.get("city", {}).get("name", ""),
            "date": e.get("dates", {}).get("start", {}).get("localDate", ""),
            "url": reverse("TicketMasterEventDetailsPage", args=[unique_id]),
            "venue": (
                e.get("_embedded", {})
                 .get("venues", [{}])[0]
                 .get("city", {})
                 .get("name", "")
            ),
        })

    return results



# def tm_search(query, size=5, city=None, date=None):
#     url = "https://app.ticketmaster.com/discovery/v2/events.json"

#     params = {
#         "apikey": settings.TICKETMASTER_API_KEY,
#         "keyword": query,
#         "size": size,
#     }

#     if city:
#         # params["city"] = city.title()
#         params["city"] = city

#     if date:
#         params["startDateTime"] = f"{date}T00:00:00Z"
#         # params["endDateTime"] = f"{date}T23:59:59Z"

#     try:
#         response = requests.get(url, params=params)
#         data = response.json()
#     except Exception:
#         return []

#     events = data.get("_embedded", {}).get("events", [])

#     return [
#         {
#             "id": e.get("id"),
#             "title": e.get("name"),
#             "type": "events",
#             # "url": f"/event_details/{e.get('id')}/",
#             "url": reverse("TicketMasterEventDetailsPage", args=[e.get("id")]),
#             "start_date": e.get("dates", {}).get("start", {}).get("localDate", ""),
#             "venue": (
#                 e.get("_embedded", {})
#                  .get("venues", [{}])[0]
#                  .get("city", {})
#                  .get("name", "")
#             ),
#         }
#         for e in events
#     ]