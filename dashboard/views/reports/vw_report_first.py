from django.views import View
from django.shortcuts import render, redirect

class ReportFirstView(View):
    def get(self, request):
        
        context = {
            'page_title' : 'Dashboard',

            'hero_banner' : True,
            'kpi_cards' : True,
            'charts_section' : True,
            'activity_events' : True,
            'bottom_section' : True,
        }
        return render(request, 'dashboard/reports/reportfirst.html', context)