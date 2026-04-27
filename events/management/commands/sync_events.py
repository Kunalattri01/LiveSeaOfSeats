from django.core.management.base import BaseCommand
from ticketmaster.services.api import fetch_events
from events.services.venue_service import get_or_create_venue
from events.services.organizer_service import get_or_create_organizer
from events.services.category_service import get_or_create_category
from events.services.event_sync_service import sync_event

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        events = fetch_events()

        for event in events:
            
            sync_event(event)
            

    # def handle(self, *args, **kwargs):
    #     events = fetch_events()

    #     for e in events:
    #         save_event(e)

    #     print("Done")