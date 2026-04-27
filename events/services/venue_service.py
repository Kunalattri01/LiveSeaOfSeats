from venues.models import Venue, City


def get_or_create_venue(api_event):

    venue_list  = api_event.get("_embedded", {}).get("venues", [])

    if not venue_list:
        print('No Venue Found')
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

    print("City:", city_name, "| Created:", city_created)


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

    print("Venue:", venue_name, "| Created:", venue_created)

    return venue