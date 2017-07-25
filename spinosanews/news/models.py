from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(unique=True)
    source = models.URLField()
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True)
    publish_date = models.DateField(default=timezone.now)
    update_date = models.DateField(auto_now=True)
    likes = models.SmallIntegerField(default=0)
    reports = models.PositiveSmallIntegerField(default=0)
    categories = models.ManyToManyField("Category")

    def __str__(self):
        return "{id}-{title}".format(id = self.id, title = self.title[0:20])

class Comment(models.Model):
    content = models.CharField(max_length=255)
    news = models.ForeignKey("News")
    publish_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    likes = models.SmallIntegerField(default=0)
    reports = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{id}-{content}".format(id = self.id,content = self.content[0:20])

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "{id}-{name}".format(id = self.id,name = self.name[0:20])



