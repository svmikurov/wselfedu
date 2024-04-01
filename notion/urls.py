from django.urls import path

from notion.views.home_view import NotionHomeView

app_name = 'notion'
urlpatterns = [
    path(
        'home/',
        NotionHomeView.as_view(),
        name='home',
    ),
]
