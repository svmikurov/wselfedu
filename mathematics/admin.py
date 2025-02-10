"""Mathematics admin panel."""

from django.contrib import admin

from mathematics.models import MathematicsAnalytic


@admin.register(MathematicsAnalytic)
class MathematicsAnalyticAdmin(admin.ModelAdmin):
    """Representation of MathematicsAnalytic model."""

    list_display = ['user', 'is_correctly', 'created_at']
    readonly_fields = [
        field.name for field in MathematicsAnalytic._meta.fields
    ]
