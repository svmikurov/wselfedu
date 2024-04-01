from django.urls import path

from config.views import HomePageView

app_name = 'notion'
urlpatterns = [
    path(
        'home/',
        HomePageView.as_view(),
        name='home',
    ),
]
