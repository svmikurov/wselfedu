from django.contrib import admin

from notion.models import (
    CategoryModel,
    NotionModel,
    SourceModel,
)


@admin.register(NotionModel)
class NotionModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'meaning', 'category', 'source']


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'descriptions']


@admin.register(SourceModel)
class SourceModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
