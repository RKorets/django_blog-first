from django.shortcuts import render, get_object_or_404
from datetime import timedelta, date


def index(request):

    return render(request, 'yumyum/index.html')
