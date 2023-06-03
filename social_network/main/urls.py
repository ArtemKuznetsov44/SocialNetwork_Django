from django.urls import path
from main.views import *

# Our app-package urls here:
urlpatterns = [
    path('',  show_start_page, name='start_page'),
    path('registration/', UserRegister.as_view(), name='registration'), 
    path('sign-in/', UserSignIn.as_view() , name='sign_in'),
    path('profile/<int:pk>', ShowProfile.as_view(), name='profile')
]