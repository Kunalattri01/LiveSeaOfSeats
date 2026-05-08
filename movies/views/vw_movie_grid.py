from django.views import View
from django.shortcuts import render, redirect

class MovieGridView(View):
    def get(self, request):
        return render(request, 'website/movies/movie-grid.html')