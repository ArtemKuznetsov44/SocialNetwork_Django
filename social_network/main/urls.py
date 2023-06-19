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
    path('messenger/', ShowMessengerPage.as_view(), name='messenger_page'), 
    path('messenger/dialog=<int:pk>', ShowDialogPage.as_view(), name='dialog_page'),
    path('post/id=<int:pk>', ShowOnePost.as_view(), name='one_post'),
    
    path('profile_edit_ajax/', ProfileEditingAjax.as_view(), name='edit_profile_ajax'), 
    path('photos_ajax/', AddNewPhotoAjax.as_view(), name='add_photo_ajax'), 
    path('post_ajax/', AddNewPostAjax.as_view(), name='add_post_ajax'), 
    path('comment_ajax/', AddNewCommentAjax.as_view(), name='add_comment_ajax'), 
    path('like_ajax/', AddLikeAjax.as_view(), name='add_like_ajax'), 
    path('post_delete_ajax/', DeletePostAjax.as_view(), name='delete_post_ajax'),
    path('request_ajax/', RequestAjax.as_view(), name='request_ajax'), 
    path('start_dialog_ajax/', StartDialogAjax.as_view(), name='start_dialog_ajax'), 
    path('message_ajax/', MessageAjax.as_view(), name='create_message_ajax'),
    path('photo_delete_ajax/', DeletePhotoAjax.as_view(), name='delete_photo_ajax'), 
    path('delete_frind_ajax/', DeleteFriendAjax.as_view(), name='delete_friend_ajax'), 

]