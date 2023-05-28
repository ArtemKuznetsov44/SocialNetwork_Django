from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import os

# The list is for video files extensions:
video_extensions = ['.mp4', '.gif']

# The list is for document files extensions: 
document_extenstions = ['.docx', '.odt', '.pdf', '.txt', '.xls', 'xlxs']

def user_directory_profile_image_path(instance, filename):
    # Генерируем путь для сохранения изображения: 'uploads/username/filename'
    return 'uploads/{0}/profile/{1}'.format(instance.username, filename)

def post_directory_for_upload(instance, filename): 
    return 'uploads/posts/{0}/{1}'.format(instance, filename)

def group_directory_for_upload_main_img(instance, filename): 
    return 'uploads/groups/{0}/{1}'.format(instance, filename)

# This method can find a file extesnion and return eh
def get_content_type(file_path):
    # Getting the file extension:
    extension = Path(file_path).suffix.lower()

    # Return the match ContentType model for extension:
    if extension in video_extensions:
        return ContentType.objects.get(id=1)
    elif extension in document_extenstions:
        return ContentType.objects.get(id=2)
    
    return None

# Settings model for User:
class Setting(models.Model): 
    theme = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.theme
    
# Gender model for User:
class Gender(models.Model): 
    gender = models.CharField(max_length=7, null=False)

    def __str__(self):
        return self.gender
    

# Add some new fields to base User model from Django:
class User(AbstractUser): 
    # New fields for django default User model:
    phone = models.CharField(max_length=15, null=True, blank=False)
    gender = models.OneToOneField("Gender", on_delete=models.CASCADE, null=True, blank=False)
    date_of_birth = models.DateField(null=True, blank=False)
    profile_img = models.ImageField(upload_to=user_directory_profile_image_path, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Will be created a setting_id field in model automaticaly:
    setting = models.OneToOneField("Setting", on_delete=models.CASCADE, null=True, blank=False)

    # For geting absolute url address of current model(record in DB) by pk:
    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})

# This model should contains different type names for content(video, gif, picture)
class ContentType(models.Model): 
    name = models.CharField(max_length=15, null=False, blank=False)

# This is the model for Post:
class Post(models.Model):
    content_type = models.ForeignKey('ContentType', on_delete=models.CASCADE)
    # This field is for post's content uploading (can be blank, because it may contains text only)
    content = models.FileField(upload_to=post_directory_for_upload, null=True, blank=True)
    # In our case the body with message must be in post:
    text = models.TextField(null=False, blank=False)
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
        
        # Start save method of a super class:
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("show_post", kwargs={"pk": self.pk})

# This model is used for Group model to specify the Group field - group_theme:
class GroupTheme(models.Model): 
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name
    
# This model is a Group model:
class Group(models.Model): 
    # Group admin id:
    admin = models.ForeignKey("User", on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50, null=False, blank=False)
    group_theme = models.ForeignKey("GroupTheme", on_delete=models.CASCADE)
    group_img = models.ImageField(upload_to=group_directory_for_upload_main_img, null=True)
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
    
    