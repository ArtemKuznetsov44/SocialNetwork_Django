from django.shortcuts import render
from django.views.generic import DetailView
from main.models import * 


# Create your views here.
class UserProfile(DetailView):
    model = User
    template_name = "main/profile.html"
    context_object_name = "user"


def show_start_page(request): 
    return render(request, template_name='main/start_page.html')

def sign_in(request): 
    return render(request, template_name='main/sign_in.html')

def registration(request):
    return render(request, template_name='main/registration.htm')

def show_news_page(request): 
    pass

