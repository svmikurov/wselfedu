"""Mathematics admin panel."""

from django.contrib import admin

from mathematics.models import MathematicsAnalytic


@admin.register(MathematicsAnalytic)
class MathematicsAnalyticAdmin(admin.ModelAdmin):
    """Representation of MathematicsAnalytic model."""

    list_display = ['user']
