from django.views import View
from django.shortcuts import render, redirect

class SportsView(View):
    def get(self, request):
        return render(request, 'sports/sports.html')