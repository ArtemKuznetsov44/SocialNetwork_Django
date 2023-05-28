from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import os

def user_directory_profile_image_path(instance, filename):
    # Генерируем путь для сохранения изображения: 'uploads/username/filename'
    return 'uploads/{0}/profile/{1}'.format(instance.username, filename)

class Setting(models.Model): 
    theme = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.theme
    

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

    # Will be created a setting_id field in model automaticaly:
    setting = models.OneToOneField("Setting", on_delete=models.CASCADE, null=True, blank=False)

    # For geting absolute url address of current model(record in DB) by pk:
    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
    

