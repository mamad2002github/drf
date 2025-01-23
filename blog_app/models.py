from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class BlockUser(models.Model):
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    status = models.BooleanField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="articles",blank=True,null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name="comments")
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.text[0:10]