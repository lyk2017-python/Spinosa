from django.conf.urls import url
from news.views import HomepageView, CategoryView, NewsView

urlpatterns = [
        url(r'^$', HomepageView.as_view(), name="home"),
        url(r'^category/(?P<slug>[A-Za-z0-9\-]+)$', CategoryView.as_view(), name="category"),
        url(r'^news/(?P<slug>[A-Za-z0-9\-]+)/(?P<pk>\d+)$', NewsView.as_view(), name="newsdetail"),
    ]