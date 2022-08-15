from django import template
from django.db.models import Count
from yumyum.models import Category

register = template.Library()


@register.simple_tag(name='get_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('yumyum/list_categories.html')
def show_categories():
    # categories = Category.objects.all()
    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    return {'categories': categories}