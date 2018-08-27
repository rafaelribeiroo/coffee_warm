from django.contrib.auth.models import AbstractUser
from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})

    def get_avatar(self):
        '''
        Returns the avatar photo for template.
        '''
        avatar = '%s' % (self.avatar.url)
        return avatar
