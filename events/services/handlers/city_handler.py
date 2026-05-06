# ================================
# events/services/handlers/city_handler.py
# ================================

from venues.models import City
from events.services.utils.common import normalize


def handle_city(cities_dict):

    if not cities_dict:
        return {}

    existing_cities = City.objects.all()

    # ================= EXISTING MAP =================
    cities_map = {
        (
            normalize(city.name),
            normalize(city.state_code),
            normalize(city.country_code),
        ): city
        for city in existing_cities
    }

    to_create = []

    # ================= PROCESS =================
    for row in cities_dict.values():

        raw_name = (row.get("name") or "").strip()
        raw_state_name = (row.get("state_name") or "").strip()
        raw_state_code = (row.get("state_code") or "").strip()
        raw_country_name = (row.get("country_name") or "").strip()
        raw_country_code = (row.get("country_code") or "").strip()

        # normalized only for matching
        name = normalize(raw_name)
        state_code = normalize(raw_state_code)
        country_code = normalize(raw_country_code)

        key = (
            name,
            state_code,
            country_code
        )

        if key not in cities_map:

            to_create.append(
                City(
                    name=raw_name,

                    state_name=raw_state_name,
                    state_code=raw_state_code,

                    country_name=raw_country_name,
                    country_code=raw_country_code,
                )
            )

    # ================= BULK CREATE =================
    if to_create:

        City.objects.bulk_create(
            to_create,
            batch_size=200
        )

    # ================= RELOAD =================
    all_cities = City.objects.all()

    cities_map = {
        (
            normalize(city.name),
            normalize(city.state_code),
            normalize(city.country_code),
        ): city
        for city in all_cities
    }

    return cities_map