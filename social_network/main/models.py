from pathlib import Path

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import os


# The list is for video files extensions:
video_extensions = ['.mp4', '.gif']

# The list is for document files extensions: 
document_extenstions = ['.docx', '.odt', '.pdf', '.txt', '.xls', 'xlxs']

image_extenstions = ['.jpg', '.png', '.jpeg' ]

#region Some useful functions for models:
# This method configure the path for users' avatars uploadings:
def user_directory_profile_image_path(instance, filename):
    # Генерируем путь для сохранения изображения: 'uploads/profile/username/avatar/filename'
    return 'uploads/profile/{0}/avatar/{1}'.format(instance.username, filename)

# This method configure the path for users' background images uploadings:
def user_directory_profile_back_path(instance, filename):
    # Генерируем путь для сохранения изображения: 'uploads/profile/username/backgound/filename'
    return 'uploads/profile/{0}/bacground/{1}'.format(instance.username, filename)

# This method configure the path for users' photos uploadings:
def user_directory_photo_path(instance, filename): 
    return 'uploads/profile/{0}/photos/{1}'.format(instance.user.username, filename)

# This metdo configure the path for posts' files uploadings:
def post_directory_for_upload(instance, filename): 
    return 'uploads/posts/{0}/{1}'.format(instance.pk, filename)

# This methdo configure the path for messages' different kind of files uploading:
def message_directory_for_upload(instance, filename): 
    return 'uploads/messages/{0}/{1}/{2}'.format(instance.pk, instance.content_type__name, filename)

# This method configure the path for groups' backgound image uploadings:
def group_directory_for_upload_main_img(instance, filename): 
    return 'uploads/groups/{0}/main/{1}'.format(instance.pk, filename)

# This method configure the path for groups' backgound image uploadings:
def group_directory_for_upload_back_img(instance, filename): 
    return 'uploads/groups/{0}/back/{1}'.fromat(instance.pk, filename)

# This method can find a file extesnion and return eh
def get_content_type(file_path):
    # Getting the file extension:
    extension = Path(file_path).suffix.lower()

    # Return the match ContentType model for extension:
    if extension in video_extensions:
        return ContentType.objects.get(id=1)
    elif extension in document_extenstions:
        return ContentType.objects.get(id=2)
    elif extension in image_extenstions:
        return ContentType.objects.get(id=3)
    
    return None
#endregion

# Settings model for User:
class Setting(models.Model): 
    theme = models.CharField(max_length=15, null=False, blank=False, unique=True)

    def __str__(self):
        return self.theme


# Gender model for User:
class Gender(models.Model): 
    gender = models.CharField(max_length=7, null=False, unique=True)

    def __str__(self):
        return self.gender
    

# Add some new fields to base User model from Django:
class User(AbstractUser): 
    # New fields for django default User model:
    slug = models.SlugField(null=False, unique=True, db_index=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True, blank=False)
    phone = models.CharField(max_length=15, null=True, blank=False)
    gender = models.ForeignKey("Gender", on_delete=models.CASCADE, null=True, blank=False)
    date_of_birth = models.DateField(null=True, blank=False)
    profile_img = models.ImageField(upload_to=user_directory_profile_image_path, null=True)
    profile_back_img = models.ImageField(upload_to=user_directory_profile_back_path, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # Will be created a setting_id field in model automaticaly:
    setting = models.OneToOneField("Setting", on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.username)
        
        super().save(*args, **kwargs) # Call the real save() method

    # For geting absolute url address of current model(record in DB) by pk:
    def get_absolute_url(self):
        # if (self.username is none):
        return reverse("profile", kwargs={"slug": self.slug})
        
        # return reverser('profile', kwargs={"username": self.username})

# The model for user's photos:
class UserPhoto(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_photo_path, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        unique_together = ('user', 'photo')

#The model for user's followers:
class UserFollower(models.Model): 
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='main_for_follower_user')
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name='follower_user')

    class Meta: 
        unique_together = ('user', 'follower')


# The model for user's friend requests: 
class FriendRequest(models.Model): 
    sender = models.ForeignKey("User", on_delete=models.CASCADE, null=False, related_name='sender_user') 
    to_user = models.ForeignKey("User", on_delete=models.CASCADE, null=False, related_name='receiving_user')
    is_accepted = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        unique_together = ('sender', 'to_user') 


# This model should contains different type names for content(video, gif, picture)
class ContentType(models.Model): 
    name = models.CharField(max_length=15, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
    

# This is the model for Post:
class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)
    content_type = models.ForeignKey('ContentType', on_delete=models.CASCADE, null=True, blank=True)
    # This field is for post's content uploading (can be blank, because it may contains text only)
    content = models.FileField(upload_to=post_directory_for_upload, null=True, blank=True)
    # In our case the body with message must be in post:
    text = models.TextField(null=True, blank=True)
    like_status = models.BooleanField(default=True)
    comment_status = models.BooleanField(default=True)
    # auto_now_add=True says that this value is not for changing at all, only once time it will be added: 
    created_at = models.DateTimeField(auto_now_add=True)

    # This method should be started before Post model saving:
    def save(self, *args, **kwargs):
        # if content is not None:
        if self.content: 
            # Run get_content_type method with the specified file path of content:
            content_type = get_content_type(self.content.path)
            # If prev method result is not None:
            if content_type:
                # Initialize our content_type field:
                self.content_type = content_type
        else: 
            self.content_type = None
        
        # Start save method of a super class:
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("show_post", kwargs={"pk": self.pk})


# This model is used for Group model to specify the Group field - group_theme:
class GroupTheme(models.Model): 
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
    

# This model is a Group model:
class Group(models.Model): 
    # Group admin id:
    admin = models.ForeignKey("User", on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50, null=False, blank=False)
    group_theme = models.ForeignKey("GroupTheme", on_delete=models.CASCADE)
    group_img = models.ImageField(upload_to=group_directory_for_upload_main_img, null=True)
    group_back_img = models.ImageField(upload_to=group_directory_for_upload_back_img, null=True)
    # The group description (it must be):
    group_info = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # When call this model we will see the group_name:
    def __str__(self):
        return self.group_name

    # For dynamic url creation:
    def get_absolute_url(self):
        return reverse("group", kwargs={"pk": self.pk})


# The model for group's members: 
class GroupMember(models.Model): 
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta: 
        unique_together = ('group', 'user')


# This is model for saving post's likes:
class PostLike(models.Model): 
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta: 
        unique_together = ('post', 'user')


# This is model for saving post's comments:
class PostComment(models.Model): 
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.TextField(null=False, blank=False)


# This is the model Chat:
class Chat(models.Model): 
    is_private = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("chat", kwargs={"pk": self.pk})
    

# This is the model for chat members:
class ChatMember(models.Model): 
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta: 
        unique_together = ('chat', 'user')


# This is the model for Message: 
class Message(models.Model): 
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE)
    sender = models.ForeignKey("User", on_delete=models.CASCADE)
    content_type = models.ForeignKey("ContentType", on_delete=models.CASCADE)
    content = models.FileField(upload_to=message_directory_for_upload, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    # This method should be started before Message model saving:
    def save(self, *args, **kwargs):
        # if content is not None:
        if self.content: 
            # Run get_content_type method with the specified file path of content:
            content_type = get_content_type(self.content.path)
            # If prev method result is not None:
            if content_type:
                # Initialize our content_type field:
                self.content_type = content_type
        
        # Start save method of a super class:
        super().save(*args, **kwargs)
