from django.shortcuts import render, get_object_or_404
from .models import News, Category


def index(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'News list'
    }

    return render(request, 'yumyum/index.html', context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {
        'news': news,
        'category': category,
        'title': 'News'
    }

    return render(request, 'yumyum/category.html', context)


def view_news(request, news_id: int):
    news_item = get_object_or_404(News.objects.get(pk=news_id))
    return render(request, 'yumyum/view_news.html', {'news_item': news_item})


def add_news(request):
    pass