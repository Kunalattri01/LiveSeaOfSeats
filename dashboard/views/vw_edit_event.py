from django.views import View
from django.shortcuts import render, redirect

from events.services.event_service import get_filter_categories, get_filter_language, get_filter_eventtags

class EditEventView(View):
    def get(self, request):

        context = {
            'page_title': 'Events - Add / Update',
            'dropdown_categories' : get_filter_categories(),
            'dropdown_language' : get_filter_language(),
            'dropdown_eventtags' : get_filter_eventtags(),
        }

        return render(request, 'dashboard/events/edit-event.html', context)