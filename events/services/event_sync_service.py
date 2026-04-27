from django.utils.text import slugify
from events.models import Event, EventTag, EventMedia
from booking.models import ShowTime

from .venue_service import get_or_create_venue
from .organizer_service import get_or_create_organizer
from .category_service import get_or_create_category


def sync_event(api_event):

    # get_or_create_venue(api_event)
    # get_or_create_organizer(api_event)
    # get_or_create_category(api_event)

    attraction  = api_event.get("_embedded", {}).get("attractions", [{}])

    if attraction:
        group_name = attraction[0].get("name")

    event, created = Event.objects.get_or_create(
        
    )

    # print('attraction : ', attraction)
    print('group_name : ', group_name)
