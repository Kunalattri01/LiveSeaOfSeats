from django.utils.text import slugify
from events.models import Category
from events.services.utils.common import normalize


def handle_category(categories_dict, source): # Event Category handler

    # Get all external_ids
    external_ids = list(cat.get('id') for cat in categories_dict.values())

    # fetch existing categories
    is_exists = Category.objects.filter(external_id__in = external_ids, source = source)
    existing_map = {
        (row.external_id, row.source): row
        for row in is_exists
    }


    # Fetch existing by name (fallback)
    names = [normalize(v.get("name", "Other")) for v in categories_dict.values()]

    name_qs = Category.objects.filter(name__in=names)
    name_map = {
        normalize(row.name): row
        for row in name_qs
    }


    to_create, to_update = [], []

    for v in categories_dict.values():

        external_id = v.get("id")
        name = normalize(v.get("name", "Other"))

        slug = slugify(name)

        key = (external_id, source)

        obj = existing_map.get(key)

        # fallback by name
        if not obj:
            obj = name_map.get(name)

        if obj:
            updated = False

            if obj.name != name:
                obj.name = name
                updated = True

            if obj.slug != slug:
                obj.slug = slug
                updated = True

            if not obj.external_id:
                obj.external_id = external_id
                obj.source = source
                updated = True

            if updated:
                to_update.append(obj)

        else:
            to_create.append(
                Category(name=name, slug=slug, external_id=external_id, source=source)
            )

    # Bulk create
    if to_create:
        Category.objects.bulk_create(to_create, batch_size=200)

    # Bulk update
    if to_update:
        Category.objects.bulk_update(to_update, ["name", "slug", "external_id", "source"], batch_size=200)

    return {
        (row.external_id, row.source): row
        for row in Category.objects.filter(
            external_id__in=external_ids,
            source=source
        )
    }