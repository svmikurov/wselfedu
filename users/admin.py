from django.contrib import admin

from users.models import UserModel, Mentorship, MentorshipRequest


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'is_staff', 'date_joined']
    ordering = ['date_joined']
    list_display_links = ['username']


@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    pass


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    pass
