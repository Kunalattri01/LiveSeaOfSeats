from django.views import View
from django.shortcuts import render
from ..services.event_service import get_event_details, get_speaker_details, get_selected_faqs, get_sponsors, get_event_layout

class EventDetailsView(View):
    def get(self, request, event_id):

        event_detail = get_event_details(event_id) # event details 
        faqs_detail = get_selected_faqs(event_id) # faqs for the selected event
        speaker_detail = get_speaker_details(event_id) # speaker details
        sponsors_detail = get_sponsors(event_id) # sponsors for the selected event
        event_layout = get_event_layout(event_id) # event layout

        total_days = (event_detail.end_date - event_detail.start_date).days + 1 # total days 

        context = {
            'TitleSearch' : True,
            'event_detail': event_detail,
            'speaker_detail': speaker_detail,
            'faqs_detail': faqs_detail,
            'sponsors_detail': sponsors_detail,
            'event_layout' : event_layout,
            'total_days': total_days,
        }

        return render(request, 'events/event-details.html', context)