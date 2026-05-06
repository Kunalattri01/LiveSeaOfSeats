from events.services.handlers import handle_category, handle_organizers, handle_city, handle_venue, handle_event, handle_showtime, handle_tags, handle_event_media, handle_languages, attach_tags_to_events, attach_languages_to_events

from events.services.provider import fetch_ticketmaster_events
from events.services.transformer import transform_batch


def sync_events():

    raw_data = fetch_ticketmaster_events()

    CHUNK_SIZE = 200

    for i in range(0, len(raw_data), CHUNK_SIZE):

        chunk = raw_data[i:i+CHUNK_SIZE]

        transformed_data = transform_batch(chunk) # transform only chunk data

        categories_dict, organizers_dict, venues_dict, cities_dict, event_dict, showtime_dict = {}, {}, {}, {}, {}, {}

        # ================= EXTRACT =================
        for row in transformed_data:

            if row.get('venue_data') and row['venue_data'].get("id"):
                venues_dict[row['venue_data']['id']] = row['venue_data']

            if row.get('category_data') and row['category_data'].get('id'):
                categories_dict[row["category_data"]["id"]] = row["category_data"]

            if row.get("organizer_data") and row["organizer_data"].get("external_id"):
                organizers_dict[row["organizer_data"]["external_id"]] = row["organizer_data"]
                
            if row.get("event_data") and row["event_data"].get("external_id"):
                event_dict[row["event_data"]["external_id"]] = row["event_data"]

            if row.get("showtime_data") and row["showtime_data"].get("external_id"):
                showtime_dict[row["showtime_data"]["external_id"]] = row["showtime_data"]

            if row.get("city_data") and row["city_data"].get("name"):

                key = (
                    row["city_data"]["name"],
                    row["city_data"]["state_code"],
                    row["city_data"]["country_code"]
                )

                cities_dict[key] = row["city_data"]

        category_map = handle_category(categories_dict, 'ticket_master') # handles category insertion and update
        organizer_map = handle_organizers(organizers_dict, 'ticket_master') # handles organizers insertion and update
        city_map = handle_city(cities_dict) # handles cities insertion and update
        venue_map = handle_venue(venues_dict, city_map, 'ticket_master')
        event_map = handle_event(event_dict, organizer_map, category_map, 'ticket_master')
        showtime_map = handle_showtime(showtime_dict, event_map, venue_map, 'ticket_master')
        handle_event_media(transformed_data, event_map, 'ticket_master')
        tag_map = handle_tags(transformed_data)
        attach_tags_to_events(transformed_data, event_map, tag_map, 'ticket_master')
        lang_map = handle_languages(transformed_data)
        attach_languages_to_events(transformed_data, event_map, lang_map, 'ticket_master')


        # # ================= CATEGORY =================
        # Category.objects.bulk_create([
        #     Category(
        #         name=v.get("name", "Other"),
        #         slug=slugify(v.get("name", "Other")),
        #         tm_id=v.get("id"),
        #         tm_param="segmentId",
        #     )
        #     for v in categories_dict.values()
        # ], ignore_conflicts=True)

        # default_category, _ = Category.objects.get_or_create(
        #     slug="other",
        #     defaults={"name": "Other", "tm_id": "default", "tm_param": "segmentId"}
        # )

        # # ================= ORGANIZER =================
        # Organizer.objects.bulk_create([
        #     Organizer(
        #         name=v.get("name", ""),
        #         email="external@example.com",
        #         phone="0000000000",
        #         website=v.get("website", ""),
        #         instagram=v.get("instagram", ""),
        #         facebook=v.get("facebook", ""),
        #         twitter=v.get("twitter", ""),
        #     )
        #     for v in organizers_dict.values()
        # ], ignore_conflicts=True)

        # # ================= CITY =================
        # City.objects.bulk_create([
        #     City(name=v["name"], state=v["state"], country=v["country"])
        #     for v in cities_dict.values()
        # ], ignore_conflicts=True)

        # city_map = {
        #     (c.name, c.state, c.country): c
        #     for c in City.objects.filter(name__in=[k[0] for k in cities_dict.keys()])
        # }

        # # ================= VENUE =================
        # venue_objs = []

        # for v in venues_dict.values():
        #     city_key = (
        #         v.get("city", {}).get("name", "Unknown"),
        #         f"{v.get('state', {}).get('name', '')} ({v.get('state', {}).get('stateCode', '')})",
        #         f"{v.get('country', {}).get('name', '')} ({v.get('country', {}).get('countryCode', '')})"
        #     )

        #     venue_objs.append(
        #         Venue(
        #             name=v.get('name'),
        #             city=city_map.get(city_key),
        #             address=v.get('address', {}).get("line1", ""),
        #             latitude=v.get('location', {}).get("latitude"),
        #             longitude=v.get('location', {}).get("longitude"),
        #         )
        #     )

        # Venue.objects.bulk_create(venue_objs, ignore_conflicts=True)

        # # ================= MAPS =================
        # category_map = {
        #     c.tm_id: c for c in Category.objects.filter(tm_id__in=categories_dict.keys())
        # }

        # organizer_map = {
        #     o.name: o for o in Organizer.objects.filter(name__in=[v["name"] for v in organizers_dict.values()])
        # }

        # venue_map = {
        #     v.name: v for v in Venue.objects.filter(name__in=[v["name"] for v in venues_dict.values()])
        # }

        # # ================= EVENT (FIXED) =================
        # event_dict = {}

        # for row in transformed_data:

        #     org = row.get("organizer_data")
        #     e = row.get("event_data")

        #     if not org or not e:
        #         continue

        #     group_name = org.get("name") or "General Event"

        #     if not e.get("start_date"):
        #         continue

        #     key = group_name   # ✅ FIX

        #     if key not in event_dict:

        #         category_obj = category_map.get(
        #             row.get("category_data", {}).get("id")
        #         ) or default_category

        #         event_dict[key] = Event(
        #             title=group_name,
        #             slug=slugify(group_name)[:100],
        #             description=e.get("description") or group_name,
        #             start_date=e.get("start_date"),
        #             end_date=e.get("end_date"),
        #             category=category_obj,
        #             organizer=organizer_map.get(group_name),
        #             venue=venue_map.get(row.get("venue_data", {}).get("name")),
        #             status="PUBLISHED",
        #             source_type="EXTERNAL",
        #             is_external=True,
        #         )

        # Event.objects.bulk_create(event_dict.values(), ignore_conflicts=True)

        # event_map = {
        #     e.title: e
        #     for e in Event.objects.filter(title__in=event_dict.keys())
        # }

        # # ================= SHOWTIME =================
        # showtime_objs = []

        # for row in transformed_data:

        #     s = row.get("showtime_data")
        #     org = row.get("organizer_data")

        #     if not s or not org:
        #         continue

        #     event_obj = event_map.get(org.get("name"))

        #     if not event_obj:
        #         continue

        #     showtime_objs.append(
        #         ShowTime(
        #             external_id=s.get("external_id"),
        #             event=event_obj,
        #             venue=venue_map.get(row.get("venue_data", {}).get("name")),
        #             match_title=s.get("match_title"),
        #             show_date=s.get("show_date"),
        #             start_time=s.get("show_time"),
        #             booking_url=s.get("booking_url"),
        #             layout_image_url=s.get("layout_image_url"),
        #         )
        #     )

        # ShowTime.objects.bulk_create(showtime_objs, ignore_conflicts=True)

        # # ================= MEDIA =================
        # media_objs = []

        # for row in transformed_data:

        #     org = row.get("organizer_data")
        #     event_obj = event_map.get(org.get("name"))

        #     if not event_obj:
        #         continue

        #     images = row.get("raw_images", [])

        #     banner = None
        #     thumbnail = None

        #     for img in images:
        #         ratio = img.get("ratio")
        #         width = img.get("width", 0)

        #         if ratio == "16_9":
        #             if not banner or width > banner.get("width", 0):
        #                 banner = img

        #         elif ratio == "4_3":
        #             if not thumbnail or width > thumbnail.get("width", 0):
        #                 thumbnail = img

        #     if banner:
        #         media_objs.append(
        #             EventMedia(
        #                 event=event_obj,
        #                 image_url=banner.get("url"),
        #                 media_type="BANNER"
        #             )
        #         )

        #     if thumbnail:
        #         media_objs.append(
        #             EventMedia(
        #                 event=event_obj,
        #                 image_url=thumbnail.get("url"),
        #                 media_type="THUMBNAIL"
        #             )
        #         )

        # EventMedia.objects.bulk_create(media_objs, ignore_conflicts=True)