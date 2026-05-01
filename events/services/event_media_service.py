from events.models import Event, EventMedia


def sync_event_media(api_events):

    event_map = {
        (e.title, e.start_date): e
        for e in Event.objects.all()
    }

    media_list = []

    for api_event in api_events:

        attraction = api_event.get("_embedded", {}).get("attractions", [])
        group_name = attraction[0].get("name") if attraction else "General Event"

        date_str = api_event.get("dates", {}).get("start", {}).get("dateTime")
        if not date_str:
            continue

        # match event
        event = None
        for (title, _), e in event_map.items():
            if title == group_name:
                event = e
                break

        if not event:
            continue

        images = api_event.get("images", [])

        for img in images:
            media_list.append(
                EventMedia(
                    event_id=event.id,
                    image_url=img.get("url"),
                    media_type="BANNER"
                )
            )

    EventMedia.objects.bulk_create(media_list, batch_size=500, ignore_conflicts=True)