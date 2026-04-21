from events.models import Event
from django.db.models import Q
from .search_ticketmaster import tm_search
from django.urls import reverse

def search_my_events(query, city=None, date=None):
    qs = Event.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )[:5]

    if city:
        qs = qs.filter(venue__city__name__iexact=city)

    if date:
        qs = qs.filter(start_date=date)

    return [
        {
            "id": e.id,
            "title": e.title,
            "type": "events",
            'start_date' : e.start_date,
            'venue': e.venue.name if e.venue else "",
            "url": reverse('EventDetailsPage', args=[e.id]),
            "subtitle": getattr(e, "date", "") or "",
        }
        for e in qs
    ]



def global_suggestions(query, types=None, city=None, date=None):
    if not query:
        return []

    results = []

    # 🔥 if no filters selected → show all
    if not types:
        types = ["events"]

    if "events" in types:
        results += search_my_events(query, city, date)
        results += tm_search(query, city, date)

    return results[:10]