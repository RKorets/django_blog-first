from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import News, Category
from .forms import NewsForm


# class without index def
class HomeNews(ListView):
    model = News
    template_name = 'yumyum/index.html'
    context_object_name = 'news'
    # queryset = News.objects.filter(is_published=True)
    # extra_context = {'title': 'Main page'}

    # add more data in default model
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main page'
        return context

    # add filter in queryset
    def get_queryset(self):
        # select_related підгружає category вразу щоб не робити lazy запит під час визову (менша кількість sql запитів)
        return News.objects.filter(is_published=True).select_related('category')


# class without category def
class NewsByCategory(ListView):
    model = News
    template_name = 'yumyum/category.html'
    context_object_name = 'news'
    allow_empty = False  # if empty data set not show page

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


# class without def view_news
class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'yumyum/news_detail.html'
    # pk_url_kwarg = 'news_id' - custom param in urls


# class without def add_news
class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'yumyum/add_news.html'
    # success_url = reverse_lazy('home') # переоприділяєм редірект, default redirect from model def get_absolute_url


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'News list'
#     }
#     return render(request, 'yumyum/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category,
#         'title': 'News'
#     }
#
#     return render(request, 'yumyum/category.html', context)


# def view_news(request, news_id: int):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'yumyum/view_news.html', {'news_item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # news = News.objects.create(**form.cleaned_data) # method for not form bind
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'yumyum/add_news.html', {'form': form})