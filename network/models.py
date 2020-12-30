from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    followers = models.ManyToManyField("User", default=None, related_name='follower')
    followings =  models.ManyToManyField("User", default=None, related_name="following")


class Post(models.Model):
    post = models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    date = models.DateTimeField()
    liked = models.ManyToManyField("User", default=None , related_name="liked")

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'post': self.post,
            'date': self.date,
            'liked': len(self.liked.all())
        }