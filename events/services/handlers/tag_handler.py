from django.utils.text import slugify
from events.models import EventTag


def handle_tags(transformed_data):

    tag_names = set()

    for row in transformed_data:
        tag_names.update(row.get("tags", []))

    # 🔹 clean invalid tags
    tag_names = {
        t.strip() for t in tag_names
        if t and t.strip()
    }

    # 🔹 fetch existing
    existing = EventTag.objects.filter(name__in=tag_names)
    existing_map = {t.name: t for t in existing}

    to_create = []

    seen_slugs = set()  # prevent duplicate in batch

    for name in tag_names:

        if name in existing_map:
            continue

        slug = slugify(name)

        # fallback if slug empty
        if not slug:
            slug = f"tag-{abs(hash(name))}"

        # prevent duplicate slug in same batch
        if slug in seen_slugs:
            continue

        seen_slugs.add(slug)

        to_create.append(
            EventTag(
                name=name,
                slug=slug
            )
        )

    if to_create:
        EventTag.objects.bulk_create(
            to_create,
            batch_size=200,
            ignore_conflicts=True  # safety
        )

    return {
        t.name: t
        for t in EventTag.objects.filter(name__in=tag_names)
    }







def attach_tags_to_events(transformed_data, event_map, tag_map, source):

    for row in transformed_data:

        event_data = row.get("event_data")
        if not event_data:
            continue

        event_obj = event_map.get((event_data.get("external_id"), source))
        if not event_obj:
            continue

        tag_names = row.get("tags", [])

        tag_objs = list(set([
            tag_map.get(name)
            for name in tag_names
            if tag_map.get(name)
        ]))

        if not tag_objs:
            continue

        event_obj.tags.set(tag_objs)