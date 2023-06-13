from django.urls import path
from main.views import *

# Our app-package urls here:
urlpatterns = [
    path('',  ShowStartPage.as_view(), name='start_page'),
    path('registration/', UserRegister.as_view(), name='registration'), 
    path('sign-in/', UserSignIn.as_view() , name='sign_in'),
    path('profile/<slug:slug>', ShowProfile.as_view(), name='profile'),
    path('sign-out/', UserSignOut.as_view(), name='sign_out'), 
    path('photos/', ShowPhotosPage.as_view(), name='photos_page'),
    path('friends/', ShowFriendsPage.as_view(), name='friends_page'), 

    path('profile_edit_ajax/', ProfileEditingAjax.as_view(), name='edit_profile_ajax'), 
    path('photos_ajax/', AddNewPhotoAjax.as_view(), name='add_photo_ajax'), 
    path('post_ajax/', AddNewPostAjax.as_view(), name='add_post_ajax'), 
    path('comment_ajax/', AddNewCommentAjax.as_view(), name='add_comment_ajax'), 
    path('like_ajax/', AddLikeAjax.as_view(), name='add_like_ajax'), 
    path('post_delete_ajax/', DeletePostAjax.as_view(), name='delete_post_ajax'),
    path('request_ajax/', RequestAjax.as_view(), name='request_ajax')

]