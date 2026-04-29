import requests
from django.conf import settings

def fetch_all_events():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    all_events = []
    page = 0

    while True:
        params = {
            "apikey": settings.TICKETMASTER_API_KEY,
            "size": 50,   # max allowed
            "page": page,
        }

        res = requests.get(url, params=params)
        data = res.json()

        events = data.get("_embedded", {}).get("events", [])

        if not events:
            break

        all_events.extend(events)

        print(f"Fetched page {page} | events: {len(events)}")

        page += 1

    return all_events