from django.core.management.base import BaseCommand
from ticketmaster.services.sync_api_data import fetch_all_events
from events.services.event_sync_service import sync_event
from events.models import Event

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        events = fetch_all_events()

        for event in events:
            sync_event(event)