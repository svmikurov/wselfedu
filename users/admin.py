from django.contrib import admin

from english.models import CategoryModel
from english.models import LabelModel
from english.models import LessonModel
from english.models import SourceModel
from english.models import WordModel

from users.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username',]


@admin.register(CategoryModel, SourceModel, LabelModel, LessonModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


@admin.register(WordModel)
class WordModelAdmin(admin.ModelAdmin):
    list_display = ['words_eng', 'words_rus', 'source',
                    'word_count', 'created_at']
