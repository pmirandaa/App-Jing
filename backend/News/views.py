from django.http.response import HttpResponseRedirect

from django.views import View
from django.urls import reverse
from django.shortcuts import render
from django.utils import timezone

from rest_framework import viewsets

from Person.models import Person
from Event.models import Event
from News.models import NewsCategory
from News.models import News
from News.serializers import NewsSerializer
from News.serializers import NewsCategorySerializer

class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()

class NewsCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = NewsCategorySerializer
    queryset = NewsCategory.objects.all()
class HomeNews(View):

    def get(self, request):
        person = None
        avatar = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)

                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(person=person).latest()

        categories = NewsCategory.objects.all()

        news = News.objects.all().order_by('-date')

        return render(request, 'Noticias/baseNoticias.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "avatar": avatar,
                          "categories": categories,
                          "news": news
                      })

    def post(self, request):
        category = request.POST.get('category')

        if category == "all":
            news = News.objects.all().order_by('-date')
        else:
            news = News.objects.filter(category=category).order_by('-date')

        person = None
        avatar = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)

                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(person=person).latest()

        categories = NewsCategory.objects.all()

        return render(request, 'Noticias/baseNoticias.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "avatar": avatar,
                          "categories": categories,
                          "news": news
                      })

    def get_with_error(self, request, error):
        person = None
        avatar = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)

                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(person=person).latest()

        categories = NewsCategory.objects.all()

        news = News.objects.all().order_by('-date')

        return render(request, 'Noticias/baseNoticias.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "avatar": avatar,
                          "error": error,
                          "categories": categories,
                          "news": news
                      })

    def get_with_success(self, request, success):
        person = None
        avatar = None

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = Person.objects.get(user=request.user)

                if person.has_avatar:
                    avatar = PersonAvatar.objects.filter(person=person).latest()

        categories = NewsCategory.objects.all()

        news = News.objects.all().order_by('-date')

        return render(request, 'Noticias/baseNoticias.html',
                      {
                          "name": request.user.username,
                          "person": person,
                          "avatar": avatar,
                          "success": success,
                          "categories": categories,
                          "news": news
                      })


class CreateNews(View):

    def post(self, request):
        title = request.POST.get('title')
        body = request.POST.get('body')
        resume = request.POST.get('resume')
        category = NewsCategory.objects.get(pk=request.POST.get('category'))
        image = request.FILES.get('image')

        news = News(
            title=title,
            body=body,
            event=Event.objects.all().first(),
            short_story=resume,
            date=timezone.now(),
            publisher=Person.objects.filter(user=request.user).first(),
            category=category,
            picture=image
        )

        news.save()

        return HttpResponseRedirect(reverse('news:home'))
