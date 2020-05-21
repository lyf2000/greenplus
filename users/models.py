from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.



class User(AbstractUser):
    follow = models.ManyToManyField('self', related_name='followers', null=True, blank=True, symmetrical=False)
    email = models.EmailField(_('email address'), unique=True)

    # REQUIRED_FIELDS = ['email']

    def bookmark_post(self, post_id):
        try:
            self.bookmarks.get(id=post_id)
            self.bookmarks.remove(post_id)
        except Exception as e:
            self.bookmarks.add(post_id)

        return True

    def follow_user(self, user_id):
        try:
            self.follow.get(id=user_id)
            self.follow.remove(user_id)
        except Exception as e:
            self.follow.add(user_id)