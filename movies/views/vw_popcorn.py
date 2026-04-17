from django.views import View
from django.shortcuts import render, redirect

class PopcornView(View):
    def get(self, request):

        context = {
            'TitleSearch' : True
        }

        return render(request, 'movies/popcorn.html', context)