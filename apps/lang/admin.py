"""Language discipline models administration."""

from django.contrib import admin

from apps.lang import models

# ----------------
# Word translation
# ----------------


@admin.register(models.Exercise)
class LangExerciseAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang app exercise model administration."""

    list_display = ['name']


@admin.register(models.NativeWord)
class NativeWordAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Native word model administration."""

    list_display = ['user', 'word', 'created_at']


@admin.register(models.EnglishWord)
class EnglishWordAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """English word model administration."""

    list_display = ['user', 'word', 'created_at']
    search_fields = ['word']


@admin.register(models.EnglishTranslation)
class EnglishTranslationAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """English translation model administration."""

    list_display = [
        'user',
        'foreign',
        'native',
        'progress',
        'created_at',
        'category',
        'source',
    ]


@admin.register(models.Mark)
class MarkAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang app mark model administration."""

    list_display = ['name']


@admin.register(models.TranslationMark)
class TranslationMarkAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Translation mark model administration."""

    list_display = [
        'translation',
        'mark',
        'created_at',
    ]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang app category model administration."""

    list_display = ['name']


@admin.register(models.Parameters)
class ParametersAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Word study parameters model administration."""

    list_display = [
        'user',
        'category',
        'mark',
        'start_period',
        'end_period',
    ]


@admin.register(models.TranslationSetting)
class TranslationSettingAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Translation study settings model administration."""

    list_display = [
        'user',
        'translation_order',
        'word_count',
    ]


@admin.register(models.PresentationSettings)
class PresentationSettingsAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Presentation settings model administration."""

    list_display = [
        'user',
        'question_timeout',
        'answer_timeout',
    ]


# ------------------------------------
# English language rule administration
# ------------------------------------


@admin.register(models.Rule)
class RuleAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Rule model administration."""

    list_display = [
        'title',
    ]


@admin.register(models.RuleClause)
class RuleClauseAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Rule clause model administration."""

    list_display = [
        'rule_str',
        'parent_str',
        'content',
        'exception_content',
    ]
    list_select_related = ['rule', 'parent']

    def parent_str(self, obj: models.RuleClause) -> str:
        """Get string representation of parent."""
        return str(obj.parent)

    def rule_str(self, obj: models.RuleClause) -> str:
        """Get string representation of rule."""
        return str(obj.rule)

    rule_str.short_description = 'Правило'  # type: ignore[attr-defined]
    rule_str.admin_order_field = 'rule'  # type: ignore[attr-defined]
    parent_str.short_description = 'Родительский пункт'  # type: ignore[attr-defined]
    parent_str.admin_order_field = 'parent'  # type: ignore[attr-defined]


@admin.register(models.RuleExample)
class RuleClauseExampleAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Rule clause english word model administration."""

    list_display = [
        'created_at',
        'word',
        'example_type',
        'user',
        'clause',
    ]
    search_fields = [
        'question_translation__foreign__word',
    ]

    def word(self, obj: models.RuleExample) -> str:
        """Get rule translation word."""
        return obj.translation.foreign.word


@admin.register(models.RuleTaskExample)
class RuleClauseTaskExampleAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Rule clause task model administration."""

    list_display = [
        'created_at',
        'question',
        'answer',
        'example_type',
        'user',
        'clause',
    ]
    search_fields = [
        'question_translation__foreign__word',
    ]

    def question(self, obj: models.RuleTaskExample) -> str:
        """Get rule question word."""
        return obj.question_translation.foreign.word

    def answer(self, obj: models.RuleTaskExample) -> str:
        """Get rule answer word."""
        return obj.answer_translation.foreign.word


@admin.register(models.RuleException)
class RuleExceptionAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Language rule translation exception model administration."""

    list_display = [
        'created_at',
        'question',
        'answer',
        'user',
        'rule',
    ]
    search_fields = [
        'question_translation__foreign__word',
    ]

    def question(self, obj: models.RuleException) -> str:
        """Get rule question word."""
        return obj.question_translation.foreign.word

    def answer(self, obj: models.RuleException) -> str:
        """Get rule answer word."""
        return obj.answer_translation.foreign.word


@admin.register(models.MentorshipEnglishRule)
class MentorshipEnglishRuleAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """English rule study via mentorship model administration."""

    list_display = [
        'mentor',
        'student',
        'rule',
    ]

    def mentor(self, obj: models.MentorshipEnglishRule) -> str:
        """Get mentor."""
        return obj.mentorship.mentor  # type: ignore[return-value]

    def student(self, obj: models.MentorshipEnglishRule) -> str:
        """Get mentor."""
        return obj.mentorship.student  # type: ignore[return-value]


@admin.register(models.EnglishAssignedExercise)
class EnglishAssignedExerciseAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """English exercise assign model administration."""

    list_display = ['mentorship', 'exercise']


@admin.register(models.EnglishExerciseTranslation)
class EnglishExerciseTranslationAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """English exercise translation model administration."""

    list_display = ['exercise', 'translation']
