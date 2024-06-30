from django.contrib import admin

from users.models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'is_staff', 'date_joined']
    ordering = ['date_joined']
    list_display_links = ['username']
