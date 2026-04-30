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