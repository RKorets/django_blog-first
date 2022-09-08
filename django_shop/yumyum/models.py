from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


def directory_path(instance, filename):
    return f'photos/{instance.title}/{filename}'


class Sex(models.Model):
    gender = models.CharField(max_length=150, db_index=True, verbose_name='Стать')

    def __str__(self):
        return self.gender


class CustomUserRegistration(User):
    gender = models.ForeignKey('Sex', on_delete=models.PROTECT, verbose_name='Стать')


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Контент')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')  # one add at create
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата редагування')  # update date every on object update
    photo = models.ImageField(upload_to=directory_path, verbose_name='Фото')  # upload_to='photos/%Y/%m/%d/'
    is_published = models.BooleanField(default=True, verbose_name='Опубліковано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категорія')
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-create_at']  # сортування по полю, можна по декількох полях


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Назва категорії')
    update_at_last_news = models.DateTimeField(default=timezone.now())

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})  # category - імя маршруту в urls

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['title']


class ViewsUser(models.Model):
    name = models.CharField(max_length=150, verbose_name='Імя користувача')
    news = models.ForeignKey('News', on_delete=models.PROTECT, verbose_name='новина')

    def __str__(self):
        return self.name