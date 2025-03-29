from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from config.settings import STATIC_URL, MEDIA_URL


# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/user.png')