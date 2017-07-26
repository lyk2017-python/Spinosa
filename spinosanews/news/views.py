from django.shortcuts import render
from django.views import generic
from news.models import *

# Create your views here.
class HomepageView(generic.ListView):
    model = News

class CategoryView(generic.DetailView):
    def get_queryset(self):
        return Category.objects.all()

class NewsView(generic.DetailView):
    def get_queryset(self):
        return News.objects.filter(status=1)

