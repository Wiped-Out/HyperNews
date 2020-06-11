from .views import MainPageView, ComingSoonView, ArticleView, CreateNews
from django.urls import path, re_path
from django.views.generic import RedirectView

urlpatterns = [    
    path('', ComingSoonView.as_view()),
    re_path(r'news/create/', CreateNews.as_view(), name="create"),
    re_path(r'news/(?P<int>\d+)', ArticleView.as_view(), name="article"),
    re_path(r'news/', MainPageView.as_view(), name="home"),
]