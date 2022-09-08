from django.shortcuts import render
from .models import Rubric


def testview(request):
    return render(request, "testapp/test.html", {'rybrics': Rubric.objects.all()})


def get_rubric(request):
    pass
