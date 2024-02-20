from django.contrib import admin

from english.models import CategoryModel
from english.models import LessonModel
from english.models import SourceModel
from english.models import WordModel

from english.models import WordUserKnowledgeRelation
from english.models import WordsFavoritesModel


@admin.register(CategoryModel, SourceModel, LessonModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


@admin.register(WordModel)
class WordModelAdmin(admin.ModelAdmin):
    list_display = ['words_eng', 'words_rus', 'source',
                    'word_count', 'created_at']


@admin.register(WordUserKnowledgeRelation)
class WordUserKnowledgeRelationAdmin(admin.ModelAdmin):
    list_display = ['word', 'user', 'knowledge_assessment']


@admin.register(WordsFavoritesModel)
class WordsFavoritesModelAdmin(admin.ModelAdmin):
    list_display = ['word', 'user']
