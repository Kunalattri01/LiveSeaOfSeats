from django.views import View
from django.shortcuts import render, redirect

class SignUpView(View):
    def get(self, request):

        context = {
            'HeaderSection' : True,
            'TitleSearch' : True,
            'FooterSection' : True
        }

        return render(request, 'website/accounts/sign-up.html', context)