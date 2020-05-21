from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
import json
import datetime
import random


class WelcomePage(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsView(View):
    template_name = 'news_template.html'

    def get(self, request, link, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as json_file:
            for news in json.load(json_file):
                if news['link'] == int(link):
                    return render(request, self.template_name, {'news_dict': news})


class NewsList(View):
    template_name = 'news_list_template.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('q'):
            with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as json_file:
                news_search_array = list(filter(
                    lambda x: request.GET.get('q') in x['title'],
                    json.load(json_file)
                ))
                return render(request, self.template_name,
                              context={'news_array': news_search_array})
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as json_file:
            return render(request, self.template_name,
                          context={'news_array': json.load(json_file)})


class NewsCreate(View):
    template_name = 'news_create_template.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        new_dict = {
            'created': str(datetime.datetime.now())[:-7],
            'text': request.POST.get('text'),
            'title': request.POST.get('title'),
            'link': random.randrange(1000, 1000000)
        }
        with open(settings.NEWS_JSON_PATH, 'a+', encoding='utf-8') as json_file:
            json_file.seek(json_file.tell() - 1)
            json_file.truncate()
            json_file.write(', ')
            json.dump(new_dict, json_file)
            json_file.write(']')
        return redirect('/news/')
