from events.models import EventMedia


def handle_event_media(transformed_data, event_map, source):

    to_create = []

    for row in transformed_data:

        event_data = row.get("event_data")
        if not event_data:
            print('ccccccccccccccc')
            continue

        event_obj = event_map.get((event_data.get("external_id"), source))
        if not event_obj:
            continue

        images = row.get("event_media", [])

        banner = None
        thumbnail = None

        # SAME LOGIC AS YOUR OLD CODE
        for img in images:
            ratio = img.get("ratio")
            width = img.get("width", 0)

            if ratio == "16_9":
                if not banner or width > banner.get("width", 0):
                    banner = img

            elif ratio == "4_3":
                if not thumbnail or width > thumbnail.get("width", 0):
                    thumbnail = img

        if banner and banner.get("url"):
            to_create.append(
                EventMedia(
                    event=event_obj,
                    image_url=banner.get("url"),
                    media_type="BANNER"
                )
            )

        if thumbnail and thumbnail.get("url"):
            to_create.append(
                EventMedia(
                    event=event_obj,
                    image_url=thumbnail.get("url"),
                    media_type="THUMBNAIL"
                )
            )

    # IMPORTANT
    EventMedia.objects.bulk_create(
        to_create,
        batch_size=200,
        ignore_conflicts=True
    )