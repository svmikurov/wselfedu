"""Defines Users app model administration."""

from django.contrib import admin

from apps.core.mixins.admin import UnchangeableAdminMixin

from .models import (
    AssignedExercise,
    Balance,
    CustomUser,
    Mentorship,
    MentorshipRequest,
)
from .models.transaction import Transaction


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Custom user model administration."""

    list_display = ['username', 'date_joined']
    ordering = ['username']


@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Mentorship model representation."""

    list_display = ['mentor', 'student']
    ordering = ['mentor', 'student']


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Mentorship request model representation."""

    list_display = ['from_user', 'to_user']
    ordering = ['from_user', 'to_user']


@admin.register(Balance)
class BalanceAdmin(UnchangeableAdminMixin, admin.ModelAdmin):  # type: ignore[type-arg]
    """User balance model administration."""

    list_display = ['user', 'total', 'updated_at']
    ordering = ['user']


# TODO: Fix username link
@admin.register(Transaction)
class TransactionAdmin(UnchangeableAdminMixin, admin.ModelAdmin):  # type: ignore[type-arg]
    """User balance combined transaction model administration."""

    list_display = ['user', 'amount', 'type', 'created_at']
    readonly_fields = [field.name for field in Transaction._meta.fields]


@admin.register(AssignedExercise)
class AssignedExercisesAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """User balance combined transaction model administration."""

    list_display = [
        'exercise',
        'mentor_display',
        'student_display',
        'created_at_format',
    ]
    ordering = [
        'created_at',
    ]

    def mentor_display(self, obj: AssignedExercise) -> str:
        """Display the mentor who assigned the exercise."""
        mentor: CustomUser = obj.mentorship.mentor
        if mentor:
            return str(mentor.username)
        return '-'

    def student_display(self, obj: AssignedExercise) -> str:
        """Display the student who is assigned the exercise."""
        student: CustomUser = obj.mentorship.student
        if student:
            return str(student.username)
        return '-'

    def created_at_format(self, obj: AssignedExercise) -> str:
        """Display the formated data time exercise assignment."""
        return obj.created_at.strftime('%Y/%m/%d %H:%M')

    student_display.short_description = 'Обучающийся'  # type: ignore[attr-defined]
    mentor_display.short_description = 'Наставник'  # type: ignore[attr-defined]
    created_at_format.short_description = 'Дата назначения'  # type: ignore[attr-defined]
