from django.core.management.base import BaseCommand
from ticketmaster.services.sync_api_data import fetch_all_events
from events.services.event_tag_service import sync_tags


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        events = fetch_all_events()
        sync_tags(events)