from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class ArticlePost(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    body=models.TextField()
    create_time=models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-updated',)

    def __str__(self):
        return self.title
