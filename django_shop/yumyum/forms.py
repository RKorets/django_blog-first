from django import forms
from django.utils import timezone
from .models import Category, News, CustomUserRegistration
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField, CaptchaTextInput


class ContactForm(forms.Form):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField(label='Капча')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Імя користувача',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# class UserRegisterForm(UserCreationForm):
#     username = forms.CharField(help_text='Поле підказка знизу інпута', label='Імя користувача', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label='Е-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2') # firstname , lastname


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(help_text='Поле підказка знизу інпута', label='Імя користувача', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Е-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    gender = forms.Select()

    class Meta:
        model = CustomUserRegistration
        fields = ('username', 'email', 'password1', 'password2', 'gender') # firstname , lastname
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),

        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }

    # custom validator -  start name as clean_
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match('\d', title):
            raise ValidationError('Invalid title, first not digits')
        categories_id = self.data.get('category')
        Category.objects.filter(pk=categories_id[0]).update(update_at_last_news=timezone.now())
        return title




# форма не звязана з моделю
# class NewsForm(forms.Form):
#
#     title = forms.CharField(max_length=150, label='Заголовок',
#                             widget=forms.TextInput(attrs={'class': 'form-control'}))
#
#     content = forms.CharField(label='Текст', required=False,
#                               widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
#
#     is_published = forms.BooleanField(label='Опубліковано?', initial=True, required=False)
#
#     category = forms.ModelChoiceField(empty_label='Оберіть категорію',
#                                       label='Категорія', queryset=Category.objects.all(),
#                                       widget=forms.Select(attrs={'class': 'form-control'}))