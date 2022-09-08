from django import template
from django.db.models import Count, F
from yumyum.models import Category, News
from django.core.cache import cache

from django.db.models.functions import ExtractMinute
register = template.Library()

# @register.simple_tag(name='get_categories')
# def get_categories():
#     categories = Category.objects.annotate(cnt=Count('news'), filter=F('news__is_published')).filter(
#         cnt__gt=0).order_by('-update_at_last_news')
#     return {'categories': categories}


@register.inclusion_tag('yumyum/list_categories.html', takes_context=True)
def show_categories(context):
    # categories = Category.objects.all()
    # news = News.objects.order_by('-create_at').distinct('category_id')
    # print(news)
    # categories = cache.get('categories')
    # if not categories:
    #     categories = Category.objects.annotate(cnt=Count('news'), filter=F('news__is_published')).filter(
    #         cnt__gt=0).order_by('-update_at_last_news')
    #     cache.set('categories', categories, 30)
    categories = Category.objects.filter(news__is_published=True).annotate(cnt=Count('news__is_published')).filter(
        cnt__gt=0).order_by('-update_at_last_news')
    return {'categories': categories, 'request': context['request']}