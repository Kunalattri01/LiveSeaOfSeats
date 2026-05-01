import requests
from django.conf import settings


def fetch_ticketmaster_events():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    all_events = []
    page = 0
    total_pages = 1

    while page < total_pages:
        params = {
            "apikey": settings.TICKETMASTER_API_KEY,
            "size": 50,
            "page": page,
        }

        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        total_pages = data.get("page", {}).get("totalPages", 1)

        events = data.get("_embedded", {}).get("events", [])
        if not events:
            break

        all_events.extend(events)

        print(f"Fetched page {page} | events: {len(events)}")
        page += 1

    print("TOTAL API EVENTS:", len(all_events))
    return all_events