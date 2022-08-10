from django.shortcuts import render, get_object_or_404
from datetime import timedelta, date
from .models import News


def index(request):
    news = News.objects.all()

    return render(request, 'yumyum/index.html', {'news': news})
