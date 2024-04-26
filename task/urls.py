from django.urls import path

from task import views

app_name = 'task'

urlpatterns = [
    path(
        'common-task-interface/',
        views.CommonTaskInterfaceView.as_view(),
        name='common_task_interface',
    ),
]
