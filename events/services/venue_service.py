from venues.models import Venue, City

CITY_CACHE = {}
VENUE_CACHE = {}


def get_or_create_venue(api_event):

    venue_list = api_event.get("_embedded", {}).get("venues", [])
    if not venue_list:
        return None

    venue_data = venue_list[0]

    city_name = venue_data.get("city", {}).get("name", "Unknown")
    state = venue_data.get("state", {}).get("name", "")
    country = venue_data.get("country", {}).get("name", "")

    city_key = f"{city_name}_{state}_{country}"

    if city_key in CITY_CACHE:
        city = CITY_CACHE[city_key]
    else:
        city, _ = City.objects.get_or_create(
            name=city_name,
            state=state,
            country=country,
        )
        CITY_CACHE[city_key] = city

    venue_name = venue_data.get("name")
    venue_key = f"{venue_name}_{city.id}"

    if venue_key in VENUE_CACHE:
        return VENUE_CACHE[venue_key]

    venue, _ = Venue.objects.get_or_create(
        name=venue_name,
        city=city,
    )

    VENUE_CACHE[venue_key] = venue
    return venue








from venues.models import Venue, City


def get_or_create_venue(api_event):

    venue_list  = api_event.get("_embedded", {}).get("venues", [])

    if not venue_list:
        return None

    venue_data = venue_list[0]

    # ------------------ [ City Model Data ] -----------------------
    city_name = venue_data.get("city", {}).get("name", "Unknown")

    state_dict = venue_data.get("state", {})
    state_name = f"{state_dict.get('name', '')} ({state_dict.get('stateCode', '')})"

    country_dict = venue_data.get("country", {})
    country_name = f"{country_dict.get('name', '')} ({country_dict.get('countryCode', '')})"

    city, city_created  = City.objects.get_or_create(
        name=city_name,
        state=state_name,
        country=country_name,
    )

    # ---------------- [ Venue Model Data ] ----------------
    venue_name = venue_data.get('name')
    venue_address = venue_data.get('address', {}).get("line1", "")

    longitude = venue_data.get('location', {}).get("longitude")
    latitude = venue_data.get('location', {}).get("latitude")

    venue, venue_created = Venue.objects.get_or_create(
        name=venue_name,
        city=city,
        defaults={
            "address": venue_address,
            "longitude": longitude,
            "latitude": latitude,
        }
    )

    return venue