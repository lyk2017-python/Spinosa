from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.URLField()
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True)
    publish_date = models.DateField(default=timezone.now)
    update_date = models.DateField(auto_now=True)
    likes = models.SmallIntegerField(default=0)
    reports = models.PositiveSmallIntegerField(default=0)
    categories = models.ManyToManyField("Category")

class Comment(models.Model):
    content = models.CharField(max_length=255)
    news = models.ForeignKey("News")
    publish_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    likes = models.SmallIntegerField(default=0)
    reports = models.PositiveSmallIntegerField(default=0)

class Category(models.Model):
    name = models.CharField(max_length=50)


