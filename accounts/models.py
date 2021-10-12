from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from PIL import Image

from .utils import user_directory_path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    avatar = models.ImageField(
        upload_to=user_directory_path, 
        default='user/avatar.png', 
        help_text="all uploaded profile photos will be resized to 200 * 200"
    )

    email_confirmed = models.BooleanField(default=False)
    captcha_score = models.FloatField(default=0.0)
    has_profile = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    
    


    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.avatar)
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.avatar)
    

    def __str__(self):
        return f"{self.user.username} Profile"



