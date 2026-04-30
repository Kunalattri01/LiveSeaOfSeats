from django.core.management.base import BaseCommand
from django.db import transaction
from ticketmaster.services.sync_api_data import fetch_all_events
from events.services.event_sync_service import sync_event

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        events = fetch_all_events()

        with transaction.atomic():
            for event in events:
                sync_event(event)