"""Defines Stydy app model administration."""

from django.contrib import admin

from apps.users.models import Person

from . import models


@admin.register(models.ExerciseAssigned)
class ExerciseAssignedAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
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

    def mentor_display(self, obj: models.ExerciseAssigned) -> str:
        """Display the mentor who assigned the exercise."""
        mentor: Person = obj.mentorship.mentor
        if mentor:
            return str(mentor.username)
        return '-'

    def student_display(self, obj: models.ExerciseAssigned) -> str:
        """Display the student who is assigned the exercise."""
        student: Person = obj.mentorship.student
        if student:
            return str(student.username)
        return '-'

    def created_at_format(self, obj: models.ExerciseAssigned) -> str:
        """Display the formated data time exercise assignment."""
        return obj.created_at.strftime('%Y/%m/%d %H:%M')

    mentor_display.short_description = 'Наставник'  # type: ignore[attr-defined]
    student_display.short_description = 'Обучающийся'  # type: ignore[attr-defined]
    created_at_format.short_description = 'Дата назначения'  # type: ignore[attr-defined]


@admin.register(models.ExerciseActive)
class ExerciseActiveAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Exercise activation model administration."""

    list_display = [
        'exercise',
        'is_active',
        'mentor_display',
        'student_display',
        'updated_at_format',
    ]

    def mentor_display(self, obj: models.ExerciseActive) -> str:
        """Display the mentor who assigned the exercise."""
        mentor: Person = obj.exercise.mentorship.mentor
        if mentor:
            return str(mentor.username)
        return '-'

    def student_display(self, obj: models.ExerciseActive) -> str:
        """Display the student who is assigned the exercise."""
        student: Person = obj.exercise.mentorship.student
        if student:
            return str(student.username)
        return '-'

    def created_at_format(self, obj: models.ExerciseActive) -> str:
        """Display the formated data time exercise assignment."""
        return obj.created_at.strftime('%Y/%m/%d %H:%M')

    def updated_at_format(self, obj: models.ExerciseActive) -> str:
        """Display the formated data time exercise update."""
        return obj.updated_at.strftime('%Y/%m/%d %H:%M')

    mentor_display.short_description = 'Наставник'  # type: ignore[attr-defined]
    student_display.short_description = 'Обучающийся'  # type: ignore[attr-defined]
    created_at_format.short_description = 'Дата назначения'  # type: ignore[attr-defined]
    updated_at_format.short_description = 'Дата изменения'  # type: ignore[attr-defined]


@admin.register(models.ExerciseExpiration)
class ExerciseExpirationAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Exercise expiration model administration."""

    list_display = [
        'exercise',
        'is_daily',
        'expiration_display',
        'mentor_display',
        'student_display',
        'updated_at_format',
    ]

    def mentor_display(self, obj: models.ExerciseExpiration) -> str:
        """Display the mentor who assigned the exercise."""
        mentor: Person = obj.exercise.mentorship.mentor
        if mentor:
            return str(mentor.username)
        return '-'

    def student_display(self, obj: models.ExerciseExpiration) -> str:
        """Display the student who is assigned the exercise."""
        student: Person = obj.exercise.mentorship.student
        if student:
            return str(student.username)
        return '-'

    def expiration_display(self, obj: models.ExerciseExpiration) -> str:
        """Display the formated data time exercise expiration."""
        date_time = obj.expiration
        if date_time:
            return date_time.strftime('%Y/%m/%d %H:%M')
        return '-'

    def updated_at_format(self, obj: models.ExerciseExpiration) -> str:
        """Display the formated data time exercise update."""
        return obj.updated_at.strftime('%Y/%m/%d %H:%M')

    mentor_display.short_description = 'Наставник'  # type: ignore[attr-defined]
    student_display.short_description = 'Обучающийся'  # type: ignore[attr-defined]
    expiration_display.short_description = 'Срок действия задания'  # type: ignore[attr-defined]
    updated_at_format.short_description = 'Дата изменения'  # type: ignore[attr-defined]


@admin.register(models.ExerciseTaskCount)
class ExerciseTaskCountAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Exercise task count model administration."""

    list_display = [
        'exercise',
        'count',
        'mentor_display',
        'student_display',
        'updated_at_format',
    ]

    def mentor_display(self, obj: models.ExerciseExpiration) -> str:
        """Display the mentor who assigned the exercise."""
        mentor: Person = obj.exercise.mentorship.mentor
        if mentor:
            return str(mentor.username)
        return '-'

    def student_display(self, obj: models.ExerciseExpiration) -> str:
        """Display the student who is assigned the exercise."""
        student: Person = obj.exercise.mentorship.student
        if student:
            return str(student.username)
        return '-'

    def updated_at_format(self, obj: models.ExerciseExpiration) -> str:
        """Display the formated data time exercise update."""
        return obj.updated_at.strftime('%Y/%m/%d %H:%M')

    mentor_display.short_description = 'Наставник'  # type: ignore[attr-defined]
    student_display.short_description = 'Обучающийся'  # type: ignore[attr-defined]
    updated_at_format.short_description = 'Дата изменения'  # type: ignore[attr-defined]


@admin.register(models.ExerciseTaskAward)
class ExerciseTaskAwardAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Exercise task award model administration."""

    list_display = [
        'exercise',
        'award',
        'mentor_display',
        'student_display',
        'updated_at_format',
        'exercise__id',
    ]

    def mentor_display(self, obj: models.ExerciseExpiration) -> str:
        """Display the mentor who assigned the exercise."""
        mentor: Person = obj.exercise.mentorship.mentor
        if mentor:
            return str(mentor.username)
        return '-'

    def student_display(self, obj: models.ExerciseExpiration) -> str:
        """Display the student who is assigned the exercise."""
        student: Person = obj.exercise.mentorship.student
        if student:
            return str(student.username)
        return '-'

    def updated_at_format(self, obj: models.ExerciseExpiration) -> str:
        """Display the formated data time exercise update."""
        return obj.updated_at.strftime('%Y/%m/%d %H:%M')

    mentor_display.short_description = 'Наставник'  # type: ignore[attr-defined]
    student_display.short_description = 'Обучающийся'  # type: ignore[attr-defined]
    updated_at_format.short_description = 'Дата изменения'  # type: ignore[attr-defined]


@admin.register(models.AssignationCompletes)
class AssignationCompletesAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Completion assigned task model administration."""

    list_display = [
        'assignation',
        'attempt_count',
        'success_count',
        'created_at',
        'updated_at',
    ]


@admin.register(models.Progress)
class ProgressAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Progress model administration."""

    list_display = [
        'user',
        'name',
        'study',
        'repeat',
        'examine',
        'know',
    ]
