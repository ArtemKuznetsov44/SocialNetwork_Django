from django.contrib import admin
from main.models import *

# Register your models here.
# admin.site.register(Setting)

# admin.site.register(Gender)
# admin.site.register(User)
# admin.site.register(ContentType)

# The User model registration:
@admin.register(User)
class UserAdmin(admin.ModelAdmin): 
    list_display = ['id', 'username', 'first_name', 'last_name', 'gender',  'email',  'last_login', 'created_at', 'is_staff']
    list_editable = ['is_staff']
    list_filter = ['id', 'created_at']
    search_fields = ['first_name', 'last_name', 'user_name']

# The Setting model registration:
@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin): 
    list_display = ['id', 'theme']

# The Gender model registration:
@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin): 
    list_display = ['id', 'gender']

# The ContentType model registration:
@admin.register(ContentType)
class ConetentTypeAdmin(admin.ModelAdmin): 
    list_display = ['id', 'name']

# The Post model registration:
@admin.register(Post)
class PostAdmin(admin.ModelAdmin): 
    list_display = ['id', 'user', 'group', 'content_type', 'content', 'text', 'like_status', 'comment_status', 'created_at']
    list_editable = ['like_status', 'comment_status']
    list_filter = ['id', 'created_at']
    search_fields = ['text']

# The GroupTheme model registration:
@admin.register(GroupTheme)
class GroupThemeAdmin(admin.ModelAdmin): 
    list_display = ['id', 'name']

# The Group model registration:
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin): 
    list_display = ['id', 'admin', 'group_name', 'group_theme', 'group_img', 'group_info', 'created_at']
    list_filter = ['group_theme', 'group_name', 'created_at']
    search_fields = ['id', 'group_theme', 'group_name', 'created_at']

# The PostLike model registration:
@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin): 
    list_display = ['id', 'post', 'user']

# The PostComment model registration:
@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin): 
    list_display = ['id', 'post', 'user', 'comment']

# The ChatType model registration:
@admin.register(ChatType)
class ChatTypeAdmin(admin.ModelAdmin): 
    list_display = ['id', 'name']

# The Chat model registration:
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin): 
    list_display = ['chat_type', 'created_at']

# The ChatMember model registration:
@admin.register(ChatMember)
class ChatMember(admin.ModelAdmin):
    list_display = ['id', 'chat', 'user']

