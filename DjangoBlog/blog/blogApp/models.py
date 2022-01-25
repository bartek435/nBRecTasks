from django.db import models
from django.conf import settings
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title