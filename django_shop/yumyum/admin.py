from django.contrib import admin

from .models import News, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'create_at', 'update_at', 'is_published') #список полів які будуть виводитись для перегляду
    list_display_links = ('id', 'title') #поля які будуть клікабельними як силка
    search_fields = ('title', 'content') #поля по яким можна здійснювати пошук
    list_editable = ('is_published', 'category', ) #поля які можна редагувати відразу в списку
    list_filter = ('is_published', 'category', ) #поля які можна фільтрувати


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
