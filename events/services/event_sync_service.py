from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify

from events.models import Event
from booking.models import ShowTime

from .venue_service import get_or_create_venue
from .organizer_service import get_or_create_organizer
from .category_service import get_or_create_category


def sync_events(api_events):

    print(f"🚀 Processing {len(api_events)} events...")

    new_events = []
    new_showtimes = []

    # Existing events map (to avoid duplicates)
    existing_events = {
        (e.title, e.start_date): e.id
        for e in Event.objects.all()
    }

    # Existing showtimes
    existing_showtimes = set(
        ShowTime.objects.values_list("external_id", flat=True)
    )

    # ============================================================
    # 🔹 STEP 1 — CREATE EVENTS (BULK)
    # ============================================================
    for api_event in api_events:

        venue = get_or_create_venue(api_event)
        organizer = get_or_create_organizer(api_event)
        category = get_or_create_category(api_event)

        if not venue:
            continue

        attraction = api_event.get("_embedded", {}).get("attractions", [])
        group_name = attraction[0].get("name") if attraction else "General Event"

        date_str = api_event.get("dates", {}).get("start", {}).get("dateTime")

        if not date_str:
            continue

        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            start_date = timezone.make_aware(dt)
        except:
            continue

        key = (group_name, start_date)

        # Generate slug (IMPORTANT FIX)
        slug = slugify(group_name)[:100]

        if key not in existing_events:
            new_events.append(
                Event(
                    title=group_name,
                    slug=slug,   # FIX FOR YOUR ERROR
                    start_date=start_date,
                    end_date=start_date,
                    venue_id=venue.id,
                    organizer_id=organizer.id if organizer else None,
                    category_id=category.id if category else None,
                    status='PUBLISHED',
                    source_type='EXTERNAL',
                    is_external=True,
                )
            )

    # BULK INSERT EVENTS
    Event.objects.bulk_create(
        new_events,
        batch_size=500,
        ignore_conflicts=True
    )

    print(f"Inserted {len(new_events)} events")

    # ============================================================
    # 🔹 STEP 2 — REFRESH EVENT MAP
    # ============================================================
    event_map = {
        (e.title, e.start_date): e.id
        for e in Event.objects.all()
    }

    # ============================================================
    # 🔹 STEP 3 — CREATE SHOWTIME (BULK)
    # ============================================================
    for api_event in api_events:

        venue = get_or_create_venue(api_event)

        attraction = api_event.get("_embedded", {}).get("attractions", [])
        group_name = attraction[0].get("name") if attraction else "General Event"

        date_str = api_event.get("dates", {}).get("start", {}).get("dateTime")

        if not date_str:
            continue

        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            start_date = timezone.make_aware(dt)
        except:
            continue

        event_id = event_map.get((group_name, start_date))

        if not event_id:
            continue

        external_id = api_event.get("id")

        # Skip duplicates
        if external_id in existing_showtimes:
            continue

        match_title = api_event.get("name")

        show_date_str = api_event.get('dates', {}).get('start', {}).get('localDate')
        show_time_str = api_event.get('dates', {}).get('start', {}).get('localTime')

        show_datetime = None

        try:
            if show_date_str and show_time_str:
                show_datetime = datetime.strptime(
                    f"{show_date_str} {show_time_str}",
                    "%Y-%m-%d %H:%M:%S"
                )
            elif show_date_str:
                show_datetime = datetime.strptime(show_date_str, "%Y-%m-%d")
        except:
            pass

        show_date = show_datetime.date() if show_datetime else None
        start_time = show_datetime.time() if show_datetime and show_time_str else None

        booking_url = api_event.get("url")
        layout_image_url = api_event.get("seatmap", {}).get("staticUrl")

        new_showtimes.append(
            ShowTime(
                external_id=external_id,
                event_id=event_id,   # FK FIX
                venue_id=venue.id,   # FK FIX
                match_title=match_title,
                show_date=show_date,
                start_time=start_time,
                booking_url=booking_url,
                layout_image_url=layout_image_url,
            )
        )

    # BULK INSERT SHOWTIME
    ShowTime.objects.bulk_create(
        new_showtimes,
        batch_size=500,
        ignore_conflicts=True
    )

    print(f"Inserted {len(new_showtimes)} showtimes")














from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime

from events.models import Event, EventTag, EventMedia, Language
from booking.models import ShowTime

from .venue_service import get_or_create_venue
from .organizer_service import get_or_create_organizer
from .category_service import get_or_create_category


def sync_event(api_event):

    venue = get_or_create_venue(api_event)
    organizer = get_or_create_organizer(api_event)
    category = get_or_create_category(api_event)

    # ----------------- [ event model ] ---------------------------
    attraction = api_event.get("_embedded", {}).get("attractions", [])
    group_name = attraction[0].get("name") if attraction else "General Event"

    slug = slugify(group_name)[:50]
    description = api_event.get('info') or api_event.get('pleaseNote') or group_name

    # age_limit = None
    # release_date = None
    # booking_start = None

    date_str = api_event.get('dates', {}).get('start', {}).get('dateTime')

    start_date = None
    end_date = None

    if date_str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            start_date = timezone.make_aware(dt)
            end_date = start_date
        except:
            pass

    # languages = None
    # tags = None
    # youtube_url = None
    # terms_and_conditions = None
    # refund_policy = None


    if not start_date:
        return None

    event, created = Event.objects.get_or_create(
        title=group_name,
        defaults={
            "slug": slug,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "venue": venue,
            "organizer": organizer,
            "category": category,
            "status": 'PUBLISHED',
            "source_type": 'EXTERNAL',
            "is_external": True,
            # external_id NOT used here
        }
    )



    # ----------------- [ Showtime Insertion ] ----------------------
    match_title = api_event.get("name")

    showtime_date_str = api_event.get('dates', {}).get('start', {}).get('localDate')
    showtime_time_str = api_event.get('dates', {}).get('start', {}).get('localTime')

    start_date = None

    if showtime_date_str and showtime_time_str:
        start_date = datetime.strptime(
            f"{showtime_date_str} {showtime_time_str}",
            "%Y-%m-%d %H:%M:%S"
        )
    elif showtime_date_str:
        # fallback if time is missing
        start_date = datetime.strptime(showtime_date_str, "%Y-%m-%d")

    show_date = start_date.date() if start_date else None
    start_time = start_date.time() if start_date and showtime_time_str else None

    layout_image_url = api_event.get("seatmap", {}).get('staticUrl') or None # future Cause : this is a URL (string) but field expects file Uploaded

    external_id = api_event.get("id")
    booking_url = api_event.get("url")

    showtime, st_created = ShowTime.objects.update_or_create(
        external_id=external_id,
        defaults={
            "event": event,
            "match_title": match_title,
            "show_date": show_date,
            "venue": venue,
            "start_time": start_time,
            "booking_url": booking_url,
            "layout_image_url": layout_image_url,
        }
    )


    # ------------------- [ Event Media ] -------------------
    # images = api_event.get('images', [])

    # banner_url = None

    # for img in images:
    #     if img.get('ratio') == '16_9':
    #         banner_url = img.get('url')
    #         break   # take only first banner

    # if banner_url:

    #     media, m_created = EventMedia.objects.get_or_create(
    #         event=event,
    #         image_url=banner_url,
    #         defaults={
    #             "media_type": "BANNER"
    #         }
    #     )

    # ------------------- [ Event Media Improved ] -------------------
    images = api_event.get('images', [])

    banner = None
    thumbnail = None

    for img in images:
        ratio = img.get("ratio")
        width = img.get("width", 0)

        # -------- Banner (16:9 best quality) --------
        if ratio == "16_9":
            if not banner or width > banner.get("width", 0):
                banner = img

        # -------- Thumbnail (4:3 best quality) --------
        elif ratio == "4_3":
            if not thumbnail or width > thumbnail.get("width", 0):
                thumbnail = img


    # ---------------- SAVE BANNER ----------------
    if banner:
        banner_url = banner.get("url")

        media, created = EventMedia.objects.get_or_create(
            event=event,
            image_url=banner_url,
            defaults={"media_type": "BANNER"}
        )

    # ---------------- SAVE THUMBNAIL ----------------
    if thumbnail:
        thumb_url = thumbnail.get("url")

        media, created = EventMedia.objects.get_or_create(
            event=event,
            image_url=thumb_url,
            defaults={"media_type": "THUMBNAIL"}
        )


    # ------------------- [ TAGS (M2M) ] -------------------
    classifications = api_event.get("classifications", [])

    tag_names = set()

    for cls in classifications:
        genre = cls.get("genre", {}).get("name")
        subgenre = cls.get("subGenre", {}).get("name")

        if genre:
            tag_names.add(genre)
        if subgenre:
            tag_names.add(subgenre)

    tag_objs = []

    for tag_name in tag_names:
        slug_val = slugify(tag_name)

        tag, _ = EventTag.objects.get_or_create(
            slug=slug_val,
            defaults={
                "name": tag_name,
                "tm_keyword": tag_name
            }
        )

        tag_objs.append(tag)

    if tag_objs:
        event.tags.set(tag_objs)


    # ------------------- [ LANGUAGES (M2M) ] -------------------

    locale = api_event.get("locale")  # e.g. "en-us"

    language_objs = []

    if locale:
        lang, _ = Language.objects.get_or_create(
            tm_locale=locale.lower(),
            defaults={
                "name": locale.upper(),
                "seq_no": 1
            }
        )
        language_objs.append(lang)

    if language_objs:
        event.languages.add(*language_objs)