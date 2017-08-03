from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class News(models.Model):
    ''' DOCUMENTATION
    News class is reference of the News in database.
    Title holds heading of the news, content holds the whole text,
    source holds UFL of the page, slug keeps the title as an URL,
    image gets addresses of images, publish_date and update date keeps when the entry has opened and modified,
    likes and reports hold number of their counts and
    categories as a M2M field, keeps and directs tags of entries
    Status codes: 0=pending, 1=accepted/published, 2=declined, 3=blocked '''

    title = models.CharField(max_length=200)
    content = models.TextField(unique=True)
    source = models.URLField()
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True)
    publish_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)
    likes = models.SmallIntegerField(default=0)
    reports = models.PositiveSmallIntegerField(default=0)
    status = models.PositiveSmallIntegerField(default=0)
    categories = models.ManyToManyField("Category")
    user = models.ForeignKey(User)

    def __str__(self):
        return "{id}-{title}".format(id = self.id, title = self.title[0:20])

    class Meta:
        get_latest_by = "publish_date"
        verbose_name = "News"
        verbose_name_plural = "News"

class Comment(models.Model):
    '''DOCUMENTATIONCategory
    Comment class is reference of the comments for news in database.
    Content is main text of the comment, news gets id of the News and keeps it for direction,
    publish_date and update date keeps when the comment has opened and modified,
    likes and reports hold number of their counts.'''

    content = models.CharField(max_length=255)
    news = models.ForeignKey("News")
    publish_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    likes = models.SmallIntegerField(default=0)
    reports = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(User)

    def __str__(self):
        return "{id}-{content}".format(id = self.id,content = self.content[0:20])

class Category(models.Model):
    '''DOCUMENTATION
    Category class is reference of the categories for news in database.
    name holds the keywords of tags '''

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(default="")

    def __str__(self):
        return "{id}-{name}".format(id = self.id,name = self.name[0:20])

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

@receiver(pre_save, sender = News)
@receiver(pre_save, sender = Category)
def create_slug(sender, instance, *args, **kwargs):

    if not instance.slug:
        if hasattr(sender, "name"):
            instance.slug = slugify(instance.name)
        if hasattr(sender, "title"):
            instance.slug = slugify(instance.title)
        else:
            raise AttributeError("No name or title found!")

    return instance

@receiver(pre_save, sender=News)
def auto_hidden(sender, instance, *args, **kwargs):
    if instance.reports >= 10:
        instance.status = 3 #Blocked
    return instance