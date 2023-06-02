from django.urls import path
from main.views import *

# Our app-package urls here:
urlpatterns = [
    path('',  show_start_page, name='start_page'),
    path('sign-in/', sign_in , name='sign_in'),
    path('news/', show_news_page, name='news_page'), 
    # path('profile/id=<int:pk>', UserProfile.as_view(), name='user_profile'),
]