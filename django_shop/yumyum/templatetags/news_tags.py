from django import template

from yumyum.models import Category

register = template.Library()


@register.simple_tag(name='get_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('yumyum/list_categories.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories}