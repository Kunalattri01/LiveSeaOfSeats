from django.views import View
from events.models import EventMedia, ShowTime
from django.db.models import F
from django.shortcuts import render

class TicketMasterEventDetailsView(View):
    def get(self, request, attraction_id):

        # hero_event = EventMedia.objects.select_related('event').filter(event__slug = attraction_id, media_type = 'BANNER').values(
        #         BannerURL = F('image_url'), PleaseNote = F('event__description'),
        #         EventName = F('event__title'), EventCity = F('event__venue__city__name'), EventCountry = F('event__venue__city__country'))

        hero_event = EventMedia.objects.select_related('event').filter(event__slug = attraction_id, media_type = 'BANNER').values(
                BannerURL = F('image_url'), PleaseNote = F('event__description'),
                EventName = F('event__title'), EventCity = F('event__venue__city__name'), EventCountry = F('event__venue__city__country')).first()
        
        venue_list = ShowTime.objects.select_related('event').filter(event__slug = attraction_id).values('match_title', 'show_date', 'booking_url', 'start_time')

        print('venue_list : ', venue_list)
        return render(request, 'ticketmaster/tm_event_details_new.html', {
            "event": hero_event,
            "venue": venue_list,
            'TitleSearch' : True,
            'ask_user_mail' : True,
        })