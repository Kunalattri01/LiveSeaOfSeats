from datetime import datetime
from django.utils import timezone


def safe_get_url(data, key):
    return data.get(key, [{}])[0].get("url", "") if data.get(key) else ""


def transform_event(event):

    # ================= CATEGORY =================
    classifications = event.get("classifications") or [{}]
    segment = classifications[0].get("segment") if classifications else {}

    # ================= VENUE =================
    venues = event.get("_embedded", {}).get("venues", [])
    venue_data = venues[0] if venues else {}

    venue_id = venue_data.get("id")

    # ================= CITY =================
    city_data = {}

    if venue_data:

        city_dict = venue_data.get("city", {})
        state_dict = venue_data.get("state", {})
        country_dict = venue_data.get("country", {})

        city_data = {
            "name": city_dict.get("name", "Unknown"),
            "state_name": state_dict.get("name"),
            "state_code": state_dict.get("stateCode"),
            "country_name": country_dict.get("name"),
            "country_code": country_dict.get("countryCode"),
        }

    # ================= ATTRACTION (REAL EVENT) =================
    attractions = event.get("_embedded", {}).get("attractions", [])

    event_data = {}
    organizer_data = {}

    if attractions:
        attraction = attractions[0]

        external_links = attraction.get("externalLinks", {})

        # EVENT (PARENT)
        event_data = {
            "external_id": attraction.get("id"),
            "name": attraction.get("name"),
            "description": attraction.get("name"),
            "category_id": segment.get("id")
        }

        # ORGANIZER
        organizer_data = {
            "external_id": attraction.get("id"),
            "name": attraction.get("name", "Unknown Organizer"),
            "website": attraction.get("url", ""),
            "instagram": safe_get_url(external_links, "instagram"),
            "facebook": safe_get_url(external_links, "facebook"),
            "twitter": safe_get_url(external_links, "twitter"),
        }

    # ================= SHOWTIME =================
    date_str = event.get("dates", {}).get("start", {}).get("dateTime")

    start_dt = None

    if date_str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            start_dt = timezone.make_aware(dt)
        except:
            pass

    show_date_str = event.get("dates", {}).get("start", {}).get("localDate")
    show_time_str = event.get("dates", {}).get("start", {}).get("localTime")

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

    showtime_data = {
        "external_id": event.get("id"),  # unique per show
        "event_external_id": event_data.get("external_id"),
        "venue_external_id": venue_id,
        "match_title": event.get("name"),
        "show_date": show_date,
        "show_time": show_time,
        "booking_url": event.get("url"),
        "layout_image_url": event.get("seatmap", {}).get("staticUrl"),
    }

    # ================= DESCRIPTION =================
    description = (
        event.get("info")
        or event.get("pleaseNote")
        or event.get("name")
        or "No description available"
    )

    if event_data:
        event_data["description"] = description

    # ================= LANGUAGE =================
    languages = []
    if event.get("locale"):
        languages.append(event.get("locale"))

    # ================= TAGS =================
    tag_names = set()

    for cls in classifications:
        genre = cls.get("genre", {}).get("name")
        subgenre = cls.get("subGenre", {}).get("name")

        if genre:
            tag_names.add(genre)
        if subgenre:
            tag_names.add(subgenre)

    tags = list(tag_names)

    # ================= MEDIA =================
    raw_images = event.get("images", [])

    event_media = []

    for img in raw_images:
        if img.get("url"):
            event_media.append({
                "url": img.get("url"),
                "width": img.get("width"),
                "height": img.get("height"),
                "ratio": img.get("ratio"),
            })

    # ================= FINAL =================
    return {
        "venue_data": venue_data,
        "city_data": city_data,
        "organizer_data": organizer_data,
        "category_data": segment or {},

        "event_data": event_data,
        "showtime_data": showtime_data,

        "languages": languages,
        "tags": tags,
        "event_media": event_media,
    }


def transform_batch(events):
    return [transform_event(e) for e in events]