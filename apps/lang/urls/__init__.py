"""Language discipline web urls paths."""

from . import category, mark, translation, urls
from .exercise import translation as translation_exercise

app_name = 'lang'

urlpatterns = (
    urls.urlpatterns
    + mark.urlpatterns
    + category.urlpatterns
    + translation.urlpatterns
    + translation_exercise.urlpatterns
)
