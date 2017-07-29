from django.core.mail import send_mail
from django.shortcuts import render
from django.views import generic
from news.models import *
from news.forms import ContactForm

# Create your views here.
class HomepageView(generic.ListView):
    model = News

class CategoryView(generic.DetailView):
    def get_queryset(self):
        return Category.objects.all()

class NewsView(generic.DetailView):
    def get_queryset(self):
        return News.objects.filter(status=0)

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