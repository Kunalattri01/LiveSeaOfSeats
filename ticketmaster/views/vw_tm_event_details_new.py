from django.views import View
from django.shortcuts import render
from django.core.cache import cache
from django.db.models import F

from events.models import EventMedia, ShowTime

class TicketMasterEventDetailsView(View):
    def get(self, request, attraction_id):

        # ------------------------ [ Banner data and Caching ] ------------------------
        hero_cache_key = f"hero_events_{attraction_id}"
        hero_event = cache.get(hero_cache_key)

        if hero_event is None:

            hero_event = EventMedia.objects.select_related('event').filter(event__slug = attraction_id, media_type = 'BANNER').values(
                    BannerURL = F('image_url'), PleaseNote = F('event__description'), EventCity = F('event__showtime__venue__city__name'), EventCountry = F('event__showtime__venue__city__country_code'),
                    EventName = F('event__title')).first()
            
            cache.set(hero_cache_key, hero_event, 120)



        # ------------------------ [ Events data and Caching ] ------------------------
        venue_cache_key = f"venue_list_{attraction_id}"
        venue_list = cache.get(venue_cache_key)

        if venue_list is None:
        
            venue_list = ShowTime.objects.select_related('event')\
                .filter(event__slug = attraction_id).\
                values('match_title', 'show_date', 'booking_url', 'start_time', 'venue__city__name', 'venue__city__state_name', 'venue__name')
            
            cache.set(venue_cache_key, venue_list, 60)
            
        print('venue_list : ', venue_list)
        return render(request, 'ticketmaster/tm_event_details_new.html', {
            "event": hero_event,
            "venue": venue_list,
            'TitleSearch' : True,
            'ask_user_mail' : True,
        })