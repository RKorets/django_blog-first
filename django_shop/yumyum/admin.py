from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import News, Category, Sex


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title', 'views','category', 'create_at', 'update_at', 'is_published', 'get_photo') # список полів які будуть виводитись для перегляду
    list_display_links = ('id', 'title') # поля які будуть клікабельними як силка
    search_fields = ('title', 'content') # поля по яким можна здійснювати пошук
    list_editable = ('is_published', 'category', ) # поля які можна редагувати відразу в списку
    list_filter = ('is_published', 'category', ) # поля які можна фільтрувати
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'views', ('create_at', 'update_at'))
    readonly_fields = ('get_photo', 'create_at', 'update_at')
    save_on_top = True

    # метод для рендеринга картинки в адмінці
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return 'Photo empty'

    get_photo.short_description = 'Photo in context'  # назва колонки в якій виводить фото


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Sex)
admin.site.site_title = 'Керування новинами'
admin.site.site_header = 'Керування новинами адмін панель'