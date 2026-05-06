from django.views import View
from django.shortcuts import render
from django.db.models import Prefetch
from django.core.cache import cache

from events.models import Event, EventMedia
from events.services.event_service import get_filter_categories, get_filter_language

class TicketMasterEventsPageView(View):

    def get(self, request):

        # ------------- filter caching --------------------------
        categories_filters = cache.get('categories_filters')
        if categories_filters is None:
            categories_filters = get_filter_categories()
            cache.set("categories_filters", categories_filters, 3600)


        language_filters = cache.get('language_filters')
        if language_filters is None:
            language_filters = get_filter_language()
            cache.set("language_filters", language_filters, 3600)


        country = request.session.get("country")

        cache_key = f"events_data_{country or 'all'}"
        cached_events = cache.get(cache_key)
        

        if cached_events is None:

            events = Event.objects.prefetch_related(
                        Prefetch(
                            'event_media',
                            queryset=EventMedia.objects.filter(media_type='BANNER', is_active=True),
                            to_attr='banners'
                        )
                    )
        
            if country:
                events = events.filter(
                    showtime__venue__city__country_name__iexact=country
                ).distinct()
                
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
                })

            hero_events = events_data[:8]
            events_list = events_data[:20]

            # set cache
            cache.set(cache_key, {
                "hero_events": hero_events,
                "events_list": events_list
            }, 300)

        else:
            hero_events = cached_events["hero_events"]
            events_list = cached_events["events_list"]



        return render(request, 'ticketmaster/tm_events_new.html', {
            'TitleSearch': True,
            'ask_user_mail': True,
            'hero_events': hero_events,
            'events_data': events_list,
            'categories_filters' : categories_filters, # categories filters
            'language_filters' : language_filters, # language filters
        })