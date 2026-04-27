import requests
from django.conf import settings

def fetch_events():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    params = {
        "apikey": settings.TICKETMASTER_API_KEY,
        "size" : 1,
    }

    res = requests.get(url, params=params)
    data = res.json()

    return data.get("_embedded", {}).get("events", [])