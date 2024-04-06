from django import template

from english.views.analitical_queries.analysis_data import ANALYSIS_INDICATORS

register = template.Library()


@register.filter
def humanize_indicator(value):
    return ANALYSIS_INDICATORS.get(value, 'undefined')
