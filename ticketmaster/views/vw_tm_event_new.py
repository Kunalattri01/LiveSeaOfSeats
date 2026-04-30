from django.views import View
from django.shortcuts import render
from django.db.models import Prefetch
from django.db.models import F

from events.models import Event, EventMedia
from events.services.event_service import get_filter_categories, get_filter_language

class TicketMasterEventsPageView(View):

    def get(self, request):

        country = request.session.get("country")

        events = Event.objects.select_related('venue__city')\
                .prefetch_related(
                    Prefetch(
                        'event_media',
                        queryset=EventMedia.objects.filter(media_type='BANNER', is_active=True),
                        to_attr='banners'
                    )
                )
        
        if country:
            events = events.filter(venue__city__country__iexact=country)
            
        events_data = []

        for event in events:
            banner = None

            if hasattr(event, 'banners') and event.banners:
                banner_obj = event.banners[0]

                # Prefer URL, fallback to image file
                banner = banner_obj.image_url or (
                    banner_obj.image.url if banner_obj.image else None
                )

            # fallback image (IMPORTANT)
            if not banner:
                banner = "/static/images/no-image.png"

            events_data.append({
                "Eventslug": event.slug,
                "BannerImageURL": banner,
                "EventTitle": event.title,
                "EventCity": event.venue.city.name if event.venue else None,
            })

        hero_events = events_data[:8]
        events_list = events_data[:20]
        
        return render(request, 'ticketmaster/tm_events_new.html', {
            'TitleSearch': True,
            'ask_user_mail': True,
            'hero_events': hero_events,
            'events_data': events_list,
            'categories_filters' : get_filter_categories(), # categories filters
            'language_filters' : get_filter_language(), # language filters
        })