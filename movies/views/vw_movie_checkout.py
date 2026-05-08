from django.views import View
from django.shortcuts import render, redirect

class MovieCheckoutView(View):
    def get(self, request):

        context = {
            'TitleSearch' : True
        }

        return render(request, 'website/movies/movie-checkout.html', context)