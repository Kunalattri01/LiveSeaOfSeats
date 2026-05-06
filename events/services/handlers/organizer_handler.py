from events.models import Organizer


def handle_organizers(organizers_dict, source):

    if not organizers_dict:
        return {}
    

    # Get all tm_ids
    external_ids = list(organizers_dict.keys())

    # fetch existing categories
    is_exists = Organizer.objects.filter(external_id__in = external_ids, source = source)
    existing_map = {
        (row.external_id, row.source): row 
        for row in is_exists
    }


    to_create , to_update = [], []

    for v in organizers_dict.values():

        external_id = v.get('external_id')

        if not external_id:
            continue

        name = v.get('name')
        website = v.get('website')
        instagram = v.get('instagram')
        facebook = v.get('facebook')
        twitter = v.get('twitter')

        key = (external_id, source)
        obj = existing_map.get(key)


        if obj:
            updated = False

            if obj.name != name:
                obj.name = name
                updated = True

            if obj.website != website:
                obj.website = website
                updated = True

            if obj.instagram != instagram:
                obj.instagram = instagram
                updated = True

            if obj.facebook != facebook:
                obj.facebook = facebook
                updated = True

            if obj.twitter != twitter:
                obj.twitter = twitter
                updated = True

            if updated:
                to_update.append(obj)

        else:
            to_create.append(
                Organizer(external_id = external_id, source = source, name = name, email = None, phone = None, website = website, instagram = instagram, facebook = facebook, twitter = twitter)
            )

    if to_create:
        Organizer.objects.bulk_create(to_create, batch_size=200)

    if to_update:
        Organizer.objects.bulk_update(to_update, ["name", "website", "instagram", "facebook", "twitter"], batch_size=200)

    return {
        (row.external_id, row.source): row
        for row in Organizer.objects.filter(
            external_id__in=external_ids,
            source=source
        )
    }