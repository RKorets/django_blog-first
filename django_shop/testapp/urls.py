from django.urls import path
from django.views.decorators.cache import cache_page   #

from .views import *

urlpatterns = [
    # path('', views.index, name='home'),
    path('', testview, name='test'),
    path('rubric/<int:pk>', get_rubric, name='getrubric'),
]
