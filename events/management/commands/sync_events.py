from django.core.management.base import BaseCommand
from events.services.sync_service import sync_events

class Command(BaseCommand):
    help = """
        Sync Events
    """

    def handle(self, *args, **kwargs):
        sync_events()


















# from django.core.management.base import BaseCommand
# from ticketmaster.services.sync_api_data import fetch_all_events
# from events.services.event_sync_service import sync_events
# from events.models import Event

# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         events = fetch_all_events()

#         for event in events:
#             sync_events(event)




# # from django.core.management.base import BaseCommand
# # from ticketmaster.services.sync_api_data import fetch_all_events
# # from events.services.event_sync_service import sync_events


# # class Command(BaseCommand):
# #     def handle(self, *args, **kwargs):
# #         events = fetch_all_events()
# #         print(f"Fetched {len(events)} events")

# #         sync_events(events)