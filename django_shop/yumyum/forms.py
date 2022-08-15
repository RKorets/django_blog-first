from django import forms
from .models import Category, News
import re
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
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