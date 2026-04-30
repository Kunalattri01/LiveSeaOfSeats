from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.db.models import Prefetch

from events.models import Event, EventMedia


class TicketMasterAPINewView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):

        # -------------- [ QUERY PARAMS ]-----------------
        page = int(request.GET.get('page', 1))
        category_ids = request.GET.getlist('category_id')
        language_ids = [int(i) for i in request.GET.getlist('language') if i.isdigit()]
        search = request.GET.get('search')


        # ------------ [ CACHE ]-------------------
        query_string = request.GET.urlencode()
        cache_key = f"events_{query_string}"

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        country = request.session.get("country")

        # --------------[ BASE QUERY ] -----------------
        queryset = Event.objects.select_related('venue__city')\
            .prefetch_related(
                Prefetch(
                    'event_media',
                    queryset=EventMedia.objects.filter(
                        media_type='BANNER',
                        is_active=True
                    ),
                    to_attr='banners'
                )
            ).filter(is_active=True)

        if country:
            queryset = queryset.filter(venue__city__country__iexact=country)

        # APPLY FILTERS
        if category_ids:
            queryset = queryset.filter(category_id__in=category_ids)

        if language_ids:
            queryset = queryset.filter(languages__in=language_ids)

        if search:
            queryset = queryset.filter(title__icontains=search)

        # IMPORTANT: avoid duplicates due to ManyToMany
        queryset = queryset.distinct()


        # ------------ [ PAGINATION ]-------------------
        page_size = 20
        start = (page - 1) * page_size
        end = start + page_size

        total = queryset.count()
        events = queryset[start:end]

        # -------------------------------
        # NEXT PAGE
        # -------------------------------
        next_page = None
        if end < total:
            params = request.GET.copy()
            params["page"] = page + 1
            next_page = f"/api/events/?{params.urlencode()}"

        # -------------------------------
        # SERIALIZE (MATCH FRONTEND)
        # -------------------------------
        results = []

        for event in events:

            banner = None

            if hasattr(event, 'banners') and event.banners:
                banner_obj = event.banners[0]
                banner = banner_obj.image_url or (
                    banner_obj.image.url if banner_obj.image else None
                )

            if not banner:
                banner = "/static/images/no-image.png"

            results.append({
                "id": event.slug,   # keep slug for routing
                "name": event.title,
                "image": banner,
                "city": event.venue.city.name if event.venue else None,
                "date": event.start_date.date() if event.start_date else None,
                "time": event.start_date.time() if event.start_date else None,
            })

        response_data = {
            "next": next_page,
            "results": results
        }

        # -------------- [ CACHE STORE ] -----------------
        cache.set(cache_key, response_data, timeout=300)

        return Response(response_data)
    