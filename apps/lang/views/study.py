"""English translation study view."""

from django.views import generic

from . import context


class EnglishTranslationStudyView(generic.TemplateView):
    """English translation study view."""

    template_name = 'lang/translation_study.html'
    extra_context = context.TRANSLATION_CONTEXT['english_study']
