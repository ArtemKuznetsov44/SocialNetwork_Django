from django.urls import path
from main.views import UserProfile

# Our app-package urls here:
urlpatterns = [
    path('profile/id=<int:pk>', UserProfile.as_view(), name='user_profile'),
]