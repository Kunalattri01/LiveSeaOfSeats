from django.views import View
from django.shortcuts import render
from events.services.event_service import get_venues_list
from collections import defaultdict


def convert_to_dict(d):
    if isinstance(d, defaultdict):
        d = {k: convert_to_dict(v) for k, v in d.items()}
    return d


class EventTimingView(View):

    def get(self, request, event_id):

        grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        showtimes = get_venues_list(event_id) # show venue and timing

        for show in showtimes:

            venue_id = show.get('VenueId')
            venue_name = show.get('VenueName')

            city_name = show.get('CityName')
            show_date = show.get('ShowDate')
            start_timing = show.get('StartTime')
            VenueAddress = show.get('VenueAddress')
            end_timing = show.get('EndTime')
            ShowId = show.get('ShowId')

            grouped_data[city_name][venue_name][show_date].append({
                "ShowId": ShowId,
                "venue_id": venue_id,
                "VenueAddress": VenueAddress,
                "start_timing": start_timing,
                "end_timing": end_timing,
            })

        context = {
            'TitleSearch' : True,
            'FooterSection' : True,
            'grouped_shows' : convert_to_dict(grouped_data),
        }

        return render(request, 'events/event-timing.html', context)