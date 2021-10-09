from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    title = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Like(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.post} liked by {self.liked_by}"
