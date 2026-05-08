from django.views import View
from django.shortcuts import redirect, render

class HomeView(View):
    def get(self, request):
        return render(request, 'website/users/index.html')