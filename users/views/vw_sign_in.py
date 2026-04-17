from django.views import View
from django.shortcuts import render, redirect

class SignInView(View):
    def get(self, request):

        context = {
            'HeaderSection' : True,
            'TitleSearch' : True,
            'FooterSection' : True
        }

        return render(request, 'accounts/sign-in.html', context)