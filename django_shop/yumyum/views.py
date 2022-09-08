from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.db.models import F

from .models import News, Category, ViewsUser
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .utils import MyMixin


def mail_send(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['content']
            mail = send_mail(subject, message, 'youemail@ukr.net', [email, ], fail_silently=True)
            if mail:
                messages.success(request, 'Success send!')
                return redirect('mail')
            else:
                messages.error(request, 'Fail send')
        else:
            messages.error(request, 'Error valid from')
    else:
        form = ContactForm()
    return render(request, 'yumyum/send_mail.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # autologin після регістрації
            messages.success(request, 'Success registration!')
            return redirect('home')
        else:
            messages.error(request, 'Error registration')
    else:
        form = UserRegisterForm()
    return render(request, 'yumyum/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'yumyum/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


# class without index def
class HomeNews(MyMixin, ListView):
    model = News
    initial = {'key': 'value'}
    template_name = 'yumyum/index.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'
    paginate_by = 2
    # queryset = News.objects.filter(is_published=True)
    # extra_context = {'title': 'Main page'}

    def get(self, request, *args, **kwargs):
        # self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    # add more data in default model
    def get_context_data(self, *, object_list=None, **kwargs):
        # news = News.objects.filter(news__pk=self.kwargs.get('pk'))
        object_list = self.get_queryset()
        context = super().get_context_data(**kwargs, object_list=object_list)
        context['title'] = 'Main page'
        # context['news'] = 'news'
        context['mixin'] = self.get_prop()
        return context

    # add filter in queryset
    def get_queryset(self):
        # select_related підгружає category вразу щоб не робити lazy запит під час визову (менша кількість sql запитів)
        return News.objects.filter(is_published=True).select_related('category')


# class without category def
class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'yumyum/category.html'
    context_object_name = 'news'
    allow_empty = False  # if empty data set not show page
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['category_active_page'] = self.kwargs['category_id']
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


# class without def view_news
class ViewNews(MyMixin, DetailView):
    model = News
    context_object_name = 'news_item'
    template_name = 'yumyum/view_news.html' # default name as def name urls detail_news
    # pk_url_kwarg = 'news_id' - custom param in urls

    def get(self, request, *args, **kwargs):
        news = self.get_object()
        if request.user.is_authenticated:
            user = request.user
            unique_views = ViewsUser.objects.filter(name=user, news_id=news.pk)
            if unique_views:
                return render(request, self.template_name, {'news_item': self.get_object()})
            else:
                news.views = F('views') + 1
                news.save()
                ViewsUser.objects.create(name=user, news_id=news.pk)

        return render(request, self.template_name, {'news_item': self.get_object()})


# class without def add_news
class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'yumyum/add_news.html'
    login_url = '/admin/' # або reverse_lazy('home')  # коли не авторизований буде робити редірект при переході /add-ne/
    # raise_exception = True   # якщо не аторизований і пробувати зайти на /add-news/ буде видавати помилку 403
    # коли створили новину робить редірект
    # success_url = reverse_lazy('home') # переоприділяєм редірект, default redirect from model def get_absolute_url


# def index(request):
#     news = News.objects.all()
#     paginator = Paginator(news, 2)
#     page_num = request.GET.get('page', 1) # if request.GET.get empty default equal 1
#     page_obj = paginator.get_page(page_num)
#
#     context = {
#         'news': news,
#         'title': 'News list',
#         'page_obj': page_obj
#     }
#     return render(request, 'yumyum/send_mail.html', context)


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
