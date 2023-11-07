from django.contrib import admin
from django.utils.html import format_html

from .models import Comic, Revista

# Register your models here.
# admin.site.register(Comic)


@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):

    def preview(self, comic):
        return format_html(
            f'<img style="height: 100px" src="{comic.picture}"'
        )
    preview.short_description = 'Imagem'

    list_display = ['name', 'preview', 'criado']


@admin.register(Revista)
class RevistaAdmin(admin.ModelAdmin):
    list_display = ('base', )
