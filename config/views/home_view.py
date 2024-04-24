from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'
    extra_context = {
        'title': 'WSE: Домашняя страница',
    }
