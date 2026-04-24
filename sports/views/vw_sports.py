from django.views import View
from django.shortcuts import render, redirect

class SportsView(View):
    def get(self, request):

        context = {
            'TitleSearch' : True
        }

        return render(request, 'sports/sports.html', context)