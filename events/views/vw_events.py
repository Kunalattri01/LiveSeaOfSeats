from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage
from users.services.search_service import global_search
from ..services.event_service import get_events, get_filter_language, get_filter_categories, get_filter_eventtags

class EventView(View):

    def get(self, request):

        # get the events type (upcoming or none)
        type = request.GET.get("type")

        # filters selected by users
        categories = request.GET.getlist("cat")
        languages = request.GET.getlist("lang")
        tags = request.GET.getlist("tags")


        # get related events result
        events = get_events(type, request.session.get('city')) 
        

        query = request.GET.get("q")
        events = global_search(events, query)    

        if categories:
            events = events.filter(category__slug__in=categories)

        if languages:
            events = events.filter(languages__name__in=languages).distinct()

        if tags:
            events = events.filter(tags__slug__in=tags).distinct()


        events = events.order_by("start_date", "id")
        events = events.all()
        

        paginator = Paginator(events, 9)    # 9 events per load
        page_number = request.GET.get('page', 1)

        try:
            events_data = paginator.page(page_number)
        except EmptyPage:
            return JsonResponse({
                "html": "",
                "has_next": False
            })

        # If AJAX request (scroll load)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            html = render_to_string(
                "events/partials/event_cards.html",
                {"events_data": events_data},
                request=request
            )

            return JsonResponse({
                "html": html,
                "has_next": events_data.has_next()
            })

        context = {
            'events_data' : events_data,
            'categories_filters' : get_filter_categories(), # categories filters
            'language_filters' : get_filter_language(), # language filters
            'eventtags_filters' : get_filter_eventtags(), # eventtags filters
            'selected_categories' : categories,
            'selected_languages' : languages,
            'selected_tags' : tags,
            'TitleSearch' : True
        }

        return render(request, 'events/events.html', context)