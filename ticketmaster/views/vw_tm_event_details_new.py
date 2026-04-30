from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F

from events.models import EventMedia, ShowTime
from users.models import EventLead

class TicketMasterEventDetailsView(View):
    def get(self, request, attraction_id):

        # hero_event = EventMedia.objects.select_related('event').filter(event__slug = attraction_id, media_type = 'BANNER').values(
        #         BannerURL = F('image_url'), PleaseNote = F('event__description'),
        #         EventName = F('event__title'), EventCity = F('event__venue__city__name'), EventCountry = F('event__venue__city__country'))

        hero_event = EventMedia.objects.select_related('event').filter(event__slug = attraction_id, media_type = 'BANNER').values(
                BannerURL = F('image_url'), PleaseNote = F('event__description'),
                EventName = F('event__title'), EventCity = F('event__venue__city__name'), EventCountry = F('event__venue__city__country')).first()
        
        venue_list = ShowTime.objects.select_related('event').filter(event__slug = attraction_id).values('match_title', 'show_date', 'booking_url', 'start_time', 'venue__city__name', 'venue__city__state', 'venue__name')

        return render(request, 'ticketmaster/tm_event_details_new.html', {
            "event": hero_event,
            "venue": venue_list,
            'TitleSearch' : True,
            'ask_user_mail' : True,
        })
    

    def save_lead(request):

        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            event_id = request.POST.get("event_id")

            print('name : ', name)
            print('email : ', email)
            print('phone : ', phone)
            print('event_id : ', event_id)

            # event = None
            # if event_id:
            #     event = Event.objects.filter(id=event_id).first()

            # EventLead.objects.create(
            #     event=event,
            #     name=name,
            #     email=email,
            #     phone=phone
            # )

            # return JsonResponse({
            #     "status": "success"
            # })