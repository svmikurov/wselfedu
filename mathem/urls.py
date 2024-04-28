from django.urls import path
from django.views.generic import TemplateView

from mathem import views

app_name = 'mathem'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(
            template_name='mathem/home.html',
            extra_context={
                'title': 'Математика',
            },
        ),
        name='home',
    ),
    path(
        'select-calculations-task/',
        views.SelectMathTaskParamsView.as_view(),
        name='select_calculations_task',
    ),
]
