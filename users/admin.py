"""Admin interface of models representation."""

from django.contrib import admin

from users.models import Mentorship, MentorshipRequest, Points, UserApp
from users.models.points import UserPoint, PointTransaction


@admin.register(UserApp)
class UserAdmin(admin.ModelAdmin):
    """Representation of Users model."""

    list_display = ['pk', 'username', 'date_joined', 'last_login']
    ordering = ['-date_joined', 'username']
    list_display_links = ['username']


@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    """Representation of Mentorship model."""


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    """Representation of MentorshipRequest model."""


@admin.register(Points)
class PointsAdmin(admin.ModelAdmin):
    """Representation of Points model."""

    list_display = ['user', 'balance']
    ordering = ['-created_at']


@admin.register(UserPoint)
class UserAccountAdmin(admin.ModelAdmin):
    """Representation of user account model."""

    list_display = ['user', 'balance']


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    """Representation of user account model."""

    list_display = ['account', 'amount', 'transaction_type', 'timestamp']
    ordering = ['-timestamp']
