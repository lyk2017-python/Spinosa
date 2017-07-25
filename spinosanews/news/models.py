from django.db import models
from django.utils import timezone


class News(models.Model):
    ''' DOCUMENTATION
    Title holds heading of the news, content holds the whole text,
    source holds UFL of the page, slug keeps the title as an URL,
    image gets addresses of images, publish_date and update date keeps when the entry has opened and modified,
    likes and reports hold number of their counts and
    categories as a M2M field, keeps and directs tags of entries '''

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
    '''DOCUMENTATION
    Content is main text of the comment, news gets id of the News and keeps it for direction,
    publish_date and update date keeps when the comment has opened and modified,
    likes and reports hold number of their counts.'''

    content = models.CharField(max_length=255)
    news = models.ForeignKey("News")
    publish_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    likes = models.SmallIntegerField(default=0)
    reports = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{id}-{content}".format(id = self.id,content = self.content[0:20])

class Category(models.Model):
    '''DOCUMENTATION
    name holds the keywords of tags '''

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "{id}-{name}".format(id = self.id,name = self.name[0:20])


