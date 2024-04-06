from django.views.generic import TemplateView

from english.views.analitical_queries.analysis_data import (
    get_common_analysis_data,
    get_favorites_analytic_data,
)


class AnalysisWordUserView(TemplateView):
    """User word learning analysis view."""

    template_name = 'english/analysis/word_analysis.html'
    extra_context = {
        'title': 'Информация по изучаемым словам',
    }

    def get_context_data(self, **kwargs):
        """Add analytics data to context.
        """
        user_id = self.request.user.id
        common_analysis_data = get_common_analysis_data(user_id)
        favorites_analysis_data = get_favorites_analytic_data(user_id)

        context = super().get_context_data(**kwargs)
        context['common_analysis_data'] = common_analysis_data
        context['favorites_analysis_data'] = favorites_analysis_data
        return context
