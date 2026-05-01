from django.utils.text import slugify
from events.models import Event, EventTag


def sync_tags(api_events):

    tag_map = {}

    for api_event in api_events:
        classifications = api_event.get("classifications", [])

        for cls in classifications:
            name = cls.get("genre", {}).get("name")

            if not name:
                continue

            slug = slugify(name)

            tag, _ = EventTag.objects.get_or_create(
                slug=slug,
                defaults={"name": name}
            )

            tag_map[slug] = tag

    # attach tags (lightweight)
    for event in Event.objects.all():
        event.tags.set(tag_map.values())