from django.http import Http404
from django.shortcuts import render
from django.views import generic
from news.models import *
from news.forms import *

# Create your views here.
class HomepageView(generic.CreateView):
    form_class = CreateNewsForm
    template_name = "news/news_list.html"
    success_url = "/"

    def get_status(self):
        query = News.objects.filter(status=self.kwargs["status"])
        if query.exists():
            return query.get()
        else:
            raise Http404("Status error!!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newslist"] = News.objects.all()
        return context

class CategoryView(generic.DetailView):
    def get_queryset(self):
        return Category.objects.all()

    def get_queryset(self):
        return Category.objects.all()

class NewsView(generic.DetailView):
    def get_queryset(self):
        return News.objects.filter(status=0)

    