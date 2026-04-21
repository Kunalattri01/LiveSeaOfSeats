import requests
from django.conf import settings

def tm_search(query, size=5):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": settings.TICKETMASTER_API_KEY,
        "keyword": query,
        "size": size,
    }
    data = requests.get(url, params=params).json()
    events = data.get("_embedded", {}).get("events", [])

    # normalize here (important)
    return [
        {
            "id": e.get("id"),
            "title": e.get("name"),
            "type": "ticketmaster",
            "url": f"/events/ticketmaster/{e.get('id')}/",
            "subtitle": (
                (e.get("dates", {}).get("start", {}).get("localDate") or "")
            ),
        }
        for e in events
    ]