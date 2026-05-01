from django.core.management.base import BaseCommand
from ticketmaster.services.sync_api_data import fetch_all_events
from events.services.event_media_service import sync_event_media

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        events = fetch_all_events()
        sync_event_media(events)