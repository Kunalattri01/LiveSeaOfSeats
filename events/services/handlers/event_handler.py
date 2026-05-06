from events.models import Event
from django.utils.text import slugify


def handle_event(events_dict, organizer_map, category_map, source):

    if not events_dict:
        return {}

    external_ids = [
        e.get("external_id") for e in events_dict.values()
        if e.get("external_id")
    ]

    existing_qs = Event.objects.filter(
        external_id__in=external_ids,
        source=source
    )

    existing_map = {
        (e.external_id, e.source): e
        for e in existing_qs
    }

    to_create, to_update = [], []

    for e in events_dict.values():

        external_id = e.get("external_id")
        name = e.get("name")

        if not external_id or not name:
            continue

        slug = slugify(name)

        organizer = organizer_map.get((external_id, source))
        category = category_map.get((e.get("category_id"), source))


        key = (external_id, source)
        obj = existing_map.get(key)

        description = e.get("description", "")

        if obj:
            updated = False

            if obj.title != name:
                obj.title = name
                updated = True

            if obj.slug != slug:
                obj.slug = slug
                updated = True

            if obj.description != description:
                obj.description = description
                updated = True

            if organizer and obj.organizer != organizer:
                obj.organizer = organizer
                updated = True

            if category and obj.category != category:
                obj.category = category
                updated = True

            if updated:
                to_update.append(obj)

        else:
            # SAFETY CHECK
            if not organizer or not category:
                continue

            to_create.append(
                Event(
                    title=name,
                    slug=slug,
                    description=description,
                    organizer=organizer,
                    category=category,
                    external_id=external_id,
                    source=source,
                    status="PUBLISHED",
                )
            )

    if to_create:
        Event.objects.bulk_create(to_create, batch_size=200)

    if to_update:
        Event.objects.bulk_update(
            to_update,
            ["title", "slug", "description", "organizer", "category"],
            batch_size=200
        )

    return {
        (e.external_id, e.source): e
        for e in Event.objects.filter(
            external_id__in=external_ids,
            source=source
        )
    }