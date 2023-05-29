from django.contrib import admin
from main.models import *

# Register your models here.
# admin.site.register(Setting)

# admin.site.register(Gender)
# admin.site.register(User)
# admin.site.register(ContentType)


@admin.register(User)
class UserAdmin(admin.ModelAdmin): 
    list_display = ['id', 'username', 'first_name', 'last_name', 'gender',  'email',  'last_login', 'created_at', 'is_staff']
    list_editable = ['is_staff']
    list_filter = ['id', 'created_at']
    search_fields = ['first_name', 'last_name', 'user_name']

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin): 
    list_display = ['id', 'theme']

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin): 
    list_display = ['id', 'gender']

@admin.register(ContentType)
class ConetentTypeAdmin(admin.ModelAdmin): 
    list_display = ['id', 'name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin): 
    list_display = ['id', 'content_type', 'content', 'text', 'like_status', 'comment_status', 'created_at']
    list_editable = ['like_status', 'comment_status']
    list_filter = ['id', 'created_at']
    search_fields = ['text']

@admin.register(GroupTheme)
class GroupThemeAdmin(admin.ModelAdmin): 
    list_display = ['id', 'name']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin): 
    list_display = ['id', 'admin', 'group_name', 'group_theme', 'group_img', 'group_info', 'created_at']
    list_filter = ['group_theme', 'group_name', 'created_at']
    search_fields = ['id', 'group_theme', 'group_name', 'created_at']

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin): 
    list_display = ['id', 'post', 'user']

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin): 
    list_display = ['id', 'post', 'user', 'comment']

@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin): 
    list_display = ['id', 'user', 'post']

@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin): 
    list_display = ['id', 'group', 'post']