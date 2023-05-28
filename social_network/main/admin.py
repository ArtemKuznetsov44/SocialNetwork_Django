from django.contrib import admin
from main.models import *

# Register your models here.
admin.site.register(Setting)
admin.site.register(Gender)
admin.site.register(User)
admin.site.register(ContentType)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin): 
    list_display = ['id', 'content_type', 'content', 'text', 'like_status', 'comment_status', 'created_at']
    list_editable = ['like_status', 'comment_status']
    list_filter = ['id', 'created_at']
    search_fields = ['text']

    