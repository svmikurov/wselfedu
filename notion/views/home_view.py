from django.views.generic import TemplateView


class NotionHomeView(TemplateView):
    template_name = 'notion/home.html'
