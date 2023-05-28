from django.shortcuts import render
from django.views.generic import DetailView
from main.models import * 


# Create your views here.

class UserProfile(DetailView):
    model = User
    template_name = "main/profile.html"
    context_object_name = "user"