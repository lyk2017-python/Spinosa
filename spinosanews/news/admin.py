from django.contrib import admin
from news.models import *
# Register your models here.
#ShortNews
#Comment
#Category

class NewsInLine(admin.StackedInline):
    model = News.categories.through
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]
    inlines = [NewsInLine]

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "publish_date", "reports", "status"]
    search_fields = ["title", "slug", "source"]
    list_filter = ["categories","likes","publish_date", "status"]
    readonly_fields = ["update_date"]
    fieldsets = [
        ("Global",
         {
             "fields":[
                 ("title" , "slug"),
                 "content",
                 "likes",
                 "reports",
                 "source",
                 "image",
                 "status",
                 "categories",
             ]
         }
    ),
    (     "Dates",
          {
              "fields":[
                  "publish_date",
                  "update_date",
              ]
          }
    ),

    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass