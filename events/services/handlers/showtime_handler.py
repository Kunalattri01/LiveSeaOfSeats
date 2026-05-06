from venues.models import Venue
from events.models import ShowTime


def handle_showtime(showtime_dict, event_map, venue_map, source):

    if not showtime_dict:
        return {}

    external_ids = [
        s.get("external_id") for s in showtime_dict.values()
        if s.get("external_id")
    ]

    existing_qs = ShowTime.objects.filter(
        external_id__in=external_ids,
        source=source
    )

    existing_map = {
        (s.external_id, s.source): s
        for s in existing_qs
    }

    to_create, to_update = [], []

    for s in showtime_dict.values():

        external_id = s.get("external_id")
        if not external_id:
            continue

        event_external_id = s.get("event_external_id")
        venue_external_id = s.get("venue_external_id")

        # map event
        event_obj = event_map.get((event_external_id, source))

        # map venue
        venue_obj = venue_map.get((venue_external_id, source))

        # fallback (DB lookup)
        if not venue_obj:
            venue_obj = Venue.objects.filter(
                external_id=venue_external_id,
                source=source
            ).first()

        # CRITICAL FIX
        if not event_obj:
            print("❌ Missing event:", event_external_id)
            continue

        if not venue_obj:
            print("⚠ Skipping showtime, venue missing:", venue_external_id)
            continue   # 🚀 THIS FIX SAVES YOU

        key = (external_id, source)
        obj = existing_map.get(key)

        if obj:
            updated = False

            if obj.event_id != event_obj.id:
                obj.event = event_obj
                updated = True

            if obj.venue_id != venue_obj.id:
                obj.venue = venue_obj
                updated = True

            if obj.show_date != s.get("show_date"):
                obj.show_date = s.get("show_date")
                updated = True

            if obj.start_time != s.get("show_time"):
                obj.start_time = s.get("show_time")
                updated = True

            if obj.match_title != s.get("match_title"):
                obj.match_title = s.get("match_title")
                updated = True

            if obj.booking_url != s.get("booking_url"):
                obj.booking_url = s.get("booking_url")
                updated = True

            if obj.layout_image_url != s.get("layout_image_url"):
                obj.layout_image_url = s.get("layout_image_url")
                updated = True

            if updated:
                to_update.append(obj)

        else:
            to_create.append(
                ShowTime(
                    event=event_obj,
                    venue=venue_obj,  # ✅ always valid now
                    external_id=external_id,
                    source=source,
                    match_title=s.get("match_title"),
                    show_date=s.get("show_date"),
                    start_time=s.get("show_time"),
                    booking_url=s.get("booking_url"),
                    layout_image_url=s.get("layout_image_url"),
                    status="SCHEDULED",
                )
            )

    # insert
    if to_create:
        ShowTime.objects.bulk_create(to_create, batch_size=200)

    if to_update:
        ShowTime.objects.bulk_update(
            to_update,
            [
                "event",
                "venue",
                "show_date",
                "start_time",
                "match_title",
                "booking_url",
                "layout_image_url",
            ],
            batch_size=200
        )

    return {
        (s.external_id, s.source): s
        for s in ShowTime.objects.filter(
            external_id__in=external_ids,
            source=source
        )
    }
