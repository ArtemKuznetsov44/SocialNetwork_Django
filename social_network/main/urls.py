from django.urls import path
from main.views import *

# Our app-package urls here:
urlpatterns = [
    path('',  ShowStartPage.as_view(), name='start_page'),
    path('registration/', UserRegister.as_view(), name='registration'), 
    path('sign-in/', UserSignIn.as_view() , name='sign_in'),
    path('profile/<int:pk>', ShowProfile.as_view(), name='profile'),
    path('groups/', ShowGroups.as_view(), name='groups'),
    path('group/<int:pk>', ShowGroup.as_view(), name='group'),
    path('sign-out/', UserSignOut.as_view(), name='sign_out'), 
    path('photos/', ShowPhotosPage.as_view(), name='photos_page'),

    path('create_group_ajax/', CreateGroupAjax.as_view(), name='create_group_ajax'),
    path('photos_ajax/', AddNewPhotoAjax.as_view(), name='add_photo_ajax'), 
    path('post_ajax/', AddNewPostAjax.as_view(), name='add_post_ajax'), 
    path('comment_ajax/', AddNewCommentAjax.as_view(), name='add_comment_ajax'), 
    path('like_ajax/', AddLikeAjax.as_view(), name='add_like_ajax'), 
    path('post_delete_ajax/', DeletePostAjax.as_view(), name='delete_post_ajax')
]