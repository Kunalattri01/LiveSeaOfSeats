from django.views import View
from django.shortcuts import render, redirect

class EventsStatusView(View):
    def get(self, request):

        context = {
            'page_title': 'Events Status',
        }

        return render(request, 'dashboard/events/events_status.html', context)