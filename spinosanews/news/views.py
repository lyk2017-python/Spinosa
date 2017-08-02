from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import generic
from news.models import *
from news.forms import ContactForm, CreateNewsForm, CreateCommentForm
from django.db.models import F
from django.shortcuts import get_object_or_404

def like_news(request):
    id = request.POST.get("id", default=None)
    like = request.POST.get("like")
    obj = get_object_or_404(News, id=int(id))
    if like == "true":
        obj.likes = F("likes")+1
        obj.save(update_fields=["likes"])
    elif like == "false":
        obj.likes = F("likes")-1
        obj.save(update_fields=["likes"])
    else:
        return  HttpResponse(status=400)
    obj.refresh_from_db()
    return JsonResponse({"like": obj.likes, "id": id})

def like_comments(request):
    id = request.POST.get("id", default=None)
    like = request.POST.get("like")
    obj = get_object_or_404(Comment, id=int(id))
    if like == "true":
        obj.likes = F("likes")+1
        obj.save(update_fields=["likes"])
    elif like == "false":
        obj.likes = F("likes")-1
        obj.save(update_fields=["likes"])
    else:
        return  HttpResponse(status=400)
    obj.refresh_from_db()
    return JsonResponse({"like": obj.likes, "id": id})


class CreateNewsForm(LoginRequiredMixin,generic.CreateView):
    form_class = CreateNewsForm
    template_name = "news/create_news.html"
    success_url = "/"

# Create your views here.
class HomepageView(generic.ListView):

    def get_queryset(self):
        return News.objects.filter(status=0).order_by("-publish_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newslist"] = News.objects.filter(status=0).order_by("-publish_date")
        return context

class CategoryView(generic.DetailView):
    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newslist"] = News.objects.filter(status=0, categories__slug=self.kwargs["slug"]).order_by("-publish_date")
        return context

class NewsView(generic.CreateView):
    form_class = CreateCommentForm
    template_name = "news/news_detail.html"
    success_url = "."

    def get_news(self):
        query = News.objects.filter(slug=self.kwargs["slug"], status=0)
        if query.exists():
            return query.get()
        else:
            raise Http404("News not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commentslist"] = Comment.objects.filter(news__pk=self.kwargs["pk"]).order_by("publish_date")
        context["news"] = News.objects.filter(status=0, slug=self.kwargs["slug"]).first()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PUT"]:
            post_data = kwargs["data"].copy()
            post_data["news"] = self.get_news().id
            kwargs["data"] = post_data
        return kwargs

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super().post(request,*args,**kwargs)

class ContactFormView(generic.FormView):
    form_class = ContactForm
    template_name = "news/contact.html"
    success_url = "/"

    def form_valid(self, form):
        data = form.cleaned_data
        from django.conf import settings
        send_mail(
            "Spinosa ContactForm : {}".format(data["title"]),
            ("There is a notification for you/n"
            "{}/n"
            "email={}/n"
            "ip={}").format(data["body"], data["email"], self.request.META["REMOTE_ADDR"]),
            settings.DEFAULT_FROM_EMAIL,
            ["spinosa@spinosamail.com"])
        return super().form_valid(form)