from django.contrib import admin

from glossary.models import Glossary, GlossaryCategory


@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    list_display = ['term', 'definition', 'created_at']


@admin.register(GlossaryCategory)
class GlossaryCategoryAdmin(admin.ModelAdmin):
    pass