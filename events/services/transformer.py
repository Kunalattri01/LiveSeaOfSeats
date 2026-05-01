from datetime import datetime
from django.utils import timezone


def safe_get_url(data, key):
    return data.get(key, [{}])[0].get("url", "") if data.get(key) else ""


def transform_event(event):

    # --- CATEGORY ---
    classifications = event.get("classifications") or [{}]
    segment = classifications[0].get("segment") if classifications else {}

    # --- VENUE ---
    venues = event.get("_embedded", {}).get("venues", [])
    venue_data = venues[0] if venues else {}

    # --- CITY ---
    city_data = {}

    if venue_data:
        city_dict = venue_data.get("city", {})
        state_dict = venue_data.get("state", {})
        country_dict = venue_data.get("country", {})

        city_data = {
            "name": city_dict.get("name", "Unknown"),
            "state": f"{state_dict.get('name', '')} ({state_dict.get('stateCode', '')})",
            "country": f"{country_dict.get('name', '')} ({country_dict.get('countryCode', '')})",
        }

    # --- ORGANIZER (GROUP LOGIC PRESERVED) ---
    attractions = event.get("_embedded", {}).get("attractions", [])
    organizer_data = {}

    if attractions:
        attraction = attractions[0]
        external_links = attraction.get("externalLinks", {})

        organizer_data = {
            "external_id": attraction.get("id"),
            "name": attraction.get("name", "Unknown Organizer"),
            "website": attraction.get("url", ""),
            "instagram": safe_get_url(external_links, "instagram"),
            "facebook": safe_get_url(external_links, "facebook"),
            "twitter": safe_get_url(external_links, "twitter"),
        }

    # --- EVENT EXTRA DATA ---
    date_str = event.get('dates', {}).get('start', {}).get('dateTime')

    start_date = None
    end_date = None

    if date_str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            dt = timezone.make_aware(dt)
            start_date = dt
            end_date = dt
        except:
            pass

    description = (
        event.get('info')
        or event.get('pleaseNote')
        or event.get('name')
        or "No description available"
    )

    # --- SHOWTIME DATA (PARSE PROPERLY) ---
    show_date_str = event.get('dates', {}).get('start', {}).get('localDate')
    show_time_str = event.get('dates', {}).get('start', {}).get('localTime')

    show_date = None
    show_time = None

    try:
        if show_date_str:
            show_date = datetime.strptime(show_date_str, "%Y-%m-%d").date()
    except:
        pass

    try:
        if show_time_str:
            show_time = datetime.strptime(show_time_str, "%H:%M:%S").time()
    except:
        pass

    # --- LANGUAGE ---
    languages = [event.get("locale")] if event.get("locale") else []

    # --- TAGS (IMPROVED LIKE YOUR OLD LOGIC) ---
    tag_names = set()

    for cls in event.get("classifications", []):
        genre = cls.get("genre", {}).get("name")
        subgenre = cls.get("subGenre", {}).get("name")

        if genre:
            tag_names.add(genre)
        if subgenre:
            tag_names.add(subgenre)

    tags = list(tag_names)

    # --- MEDIA (IMPORTANT FIX) ---
    raw_images = event.get("images", [])   # 👈 REQUIRED FOR YOUR SYNC

    return {
        "venue_data": venue_data,
        "city_data": city_data,
        "organizer_data": organizer_data,
        "category_data": segment or {},

        "event_data": {
            "external_id": event.get("id"),
            "name": event.get("name"),
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
        },

        "showtime_data": {
            "external_id": event.get("id"),
            "match_title": event.get("name"),
            "show_date": show_date,
            "show_time": show_time,
            "booking_url": event.get("url"),
            "layout_image_url": event.get("seatmap", {}).get("staticUrl"),
        },

        "languages": languages,
        "tags": tags,

        # 🔥 THIS IS WHAT YOUR SYNC EXPECTS
        "raw_images": raw_images,
    }


def transform_batch(events):
    return [transform_event(e) for e in events]