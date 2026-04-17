from django.views import View
from django.shortcuts import render
from events.services.event_service import get_speaker_details, selected_speaker_details

class EventSpealerView(View):
    def get(self, request, event_id, speaker_id):

        speaker_detail = get_speaker_details(event_id) # speaker details
        selected_speaker_data = selected_speaker_details(speaker_id) # selected speaker data

        context = {
            'TitleSearch' : True,
            'speaker_detail' : speaker_detail,
            'selected_speaker_data' : selected_speaker_data,
        }

        return render(request, 'events/event-speaker.html', context)