from events.models import Event
from .search_ticketmaster import tm_search


def search_my_events(query): # Search Events Db
    qs = Event.objects.filter(title__icontains=query, description__icontains = query)[:5]
    return [
        {
            "id": e.id,
            "title": e.name,
            "type": "event",
            "url": f"/events/{e.id}/",
            "subtitle": getattr(e, "date", "") or "",
        }
        for e in qs
    ]



def global_suggestions(query):
    if not query:
        return []

    results = []
    results += search_my_events(query)
    results += tm_search(query)

    return results
    # return results[:10]