# ================================
# venue_handler.py
# ================================

from venues.models import Venue, City
from events.services.utils.common import normalize
from django.db import transaction


def handle_venue(venues_dict, city_map, source):

    if not venues_dict:
        return {}

    # ================= UNKNOWN CITY =================
    unknown_city, _ = City.objects.get_or_create(
        name="Unknown",
        state_name="Unknown",
        state_code="UNK",
        country_name="Unknown",
        country_code="UNK"
    )

    external_ids = [
        v.get("id")
        for v in venues_dict.values()
        if v.get("id")
    ]

    # ================= EXISTING BY EXTERNAL =================
    existing_by_external = Venue.objects.filter(
        external_id__in=external_ids,
        source=source
    )

    external_map = {
        (v.external_id, v.source): v
        for v in existing_by_external
    }

    # ================= EXISTING BY NAME + CITY =================
    city_ids = list({
        c.id for c in city_map.values()
        if c and c.id
    })

    existing_all = Venue.objects.select_related("city").filter(
        city_id__in=city_ids
    )

    name_city_map = {
        (
            normalize(v.name),
            normalize(v.city.name),
            normalize(v.city.state_code),
            normalize(v.city.country_code),
        ): v
        for v in existing_all
    }

    to_create = []
    to_update = []

    # ================= BATCH DUPLICATE PREVENTION =================
    pending_keys = set()

    # ================= PROCESS =================
    for v in venues_dict.values():

        external_id = v.get("id")

        if not external_id:
            continue

        raw_name = (v.get("name") or "").strip()

        if not raw_name:
            continue

        name = raw_name

        norm_name = normalize(name)

        # ================= CITY =================
        city_name = normalize(
            (v.get("city", {}).get("name") or "").strip()
        )

        state_code = normalize(
            (v.get("state", {}).get("stateCode") or "").strip()
        )

        country_code = normalize(
            (v.get("country", {}).get("countryCode") or "").strip()
        )

        city_key = (
            city_name,
            state_code,
            country_code
        )

        city_obj = city_map.get(city_key)

        if not city_obj:

            print("⚠ Using Unknown city for:", name)

            city_obj = unknown_city

        # ================= LOOKUP KEYS =================
        key_ext = (external_id, source)

        key_name_city = (
            norm_name,
            normalize(city_obj.name),
            normalize(city_obj.state_code),
            normalize(city_obj.country_code),
        )

        # ================= FIND EXISTING =================
        obj = external_map.get(key_ext)

        if not obj:
            obj = name_city_map.get(key_name_city)

        # ================= ADDRESS =================
        address_data = v.get("address", {}) or {}

        address_parts = [
            address_data.get("line1", ""),
            address_data.get("line2", ""),
            address_data.get("line3", ""),
        ]

        address = ", ".join(
            part.strip()
            for part in address_parts
            if part
        )

        # ================= LOCATION =================
        location = v.get("location", {}) or {}

        latitude = (location.get("latitude") or "").strip() or None
        longitude = (location.get("longitude") or "").strip() or None

        # ================= UPDATE =================
        if obj and obj.pk:

            updated = False

            if obj.name != name:
                obj.name = name
                updated = True

            if obj.city_id != city_obj.id:
                obj.city = city_obj
                updated = True

            if obj.address != address:
                obj.address = address
                updated = True

            if str(obj.latitude) != str(latitude):
                obj.latitude = latitude
                updated = True

            if str(obj.longitude) != str(longitude):
                obj.longitude = longitude
                updated = True

            if updated:
                to_update.append(obj)

        # ================= CREATE =================
        else:

            # prevent duplicate creation in same batch
            if key_name_city in pending_keys:
                continue

            new_obj = Venue(
                external_id=external_id,
                source=source,
                name=name,
                city=city_obj,
                address=address,
                latitude=latitude,
                longitude=longitude,
            )

            to_create.append(new_obj)

            pending_keys.add(key_name_city)

    # ================= SAVE =================
    with transaction.atomic():

        # ---------- CREATE ----------
        if to_create:

            print("✅ Creating venues:", len(to_create))

            Venue.objects.bulk_create(
                to_create,
                batch_size=200
            )

        # ---------- UPDATE ----------
        valid_updates = [
            obj for obj in to_update
            if obj.pk
        ]

        if valid_updates:

            print("♻ Updating venues:", len(valid_updates))

            Venue.objects.bulk_update(
                valid_updates,
                [
                    "name",
                    "city",
                    "address",
                    "latitude",
                    "longitude"
                ],
                batch_size=200
            )

    # ================= FINAL MAP =================
    final_queryset = Venue.objects.filter(
        external_id__in=external_ids,
        source=source
    )

    final_map = {
        (v.external_id, v.source): v
        for v in final_queryset
    }

    return final_map