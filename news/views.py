from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.conf import settings
from django.forms import Form, CharField, ValidationError
import json
from datetime import datetime
from itertools import groupby

if_fails = [
    {
        "created": "2020-02-09 14:15:10",
        "text": "Text of the news 1",
        "title": "News 1",
        "link": 1
    },
    {
        "created": "2020-02-10 14:15:10",
        "text": "Text of the news 2",
        "title": "News 2",
        "link": 2
    },
    {
        "created": "2020-02-09 16:15:10",
        "text": "Text of the news 3",
        "title": "News 3",
        "link": 3
    },
    {
        "created": "2020-06-10 11:16:49",
        "text": "asdasfas",
        "title": "fasdas",
        "link": 4
    }
]

# Create your views here.
class MainPageView(View):
    class CreateForm(Form):
        q = CharField(label='Search', min_length=1, max_length=20)

    def get(self, request, *args, **kwargs):
        try:
            with open(settings.NEWS_JSON_PATH, 'r') as json_file:
                news_from_json = json.load(json_file)
                query = request.GET.get('q')
                data = dict()
                if query is not None:
                    news_from_json = [x for x in news_from_json if query in x['title']]
                    if len(news_from_json) >= 1:
                        data = {'count': len(news_from_json), 'q': query}
                    else: 
                        return render(request, 'news/newshome.html', context={'q': query, 'form': self.CreateForm})
                return render(request, 'news/newshome.html', context={'data': data, 'news': news_from_json, 'form': self.CreateForm})

        except json.JSONDecodeError:
            return redirect('/news/create')

class ArticleView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('='*9)
        print('Getting context data...')
        print(context)
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            try:
                news_from_json = json.load(json_file)
                art_link = int(kwargs['int'])
                art = [n for n in news_from_json if n['link'] == art_link][0]
                context['title'] = art['title']
                context['text'] = art['text']
                context['created'] = art['created']
                return context
            except IndexError:
                raise Http404

class CreateNews(CreateView):
    js = None

    class CreateForm(Form):
        title = CharField(label= 'Enter title',min_length=1, max_length=30)
        text = CharField(label='Enter text', max_length=1024)
    
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html', context={'form': self.CreateForm})

    def post(self, request, *args, **kwargs):
        form = self.CreateForm(request.POST)
        if form.is_valid():
            try:
                with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as read_file:
                    self.js = json.load(read_file)
                    used_links = [x['link'] for x in self.js]
                    link = 1
                    while link in used_links:
                        link += 1
                with open(settings.NEWS_JSON_PATH, 'w', encoding='utf-8') as json_news:
                    title, text, time = form.cleaned_data['title'], form.cleaned_data['text'], str(datetime.now())[:-7]
                    print('='*9)
                    print(title, text)
                    self.js.append({'created': time, 'text': text, 'title': title, 'link': link})
                    json.dump(self.js, json_news, indent=4)
                return redirect('/news/')

            except json.JSONDecodeError:
                print('='*9)
                print('whoops...')
                with open(settings.NEWS_JSON_PATH, 'w') as pepeg:
                    json.dump(if_fails, pepeg, indent=4)
                raise ValidationError('Empty Json')

class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')
