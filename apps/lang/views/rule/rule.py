"""Language rule views."""

from django.views import generic


class RuleIndexView(generic.TemplateView):
    """Language rule create view."""

    template_name = 'lang/rule/index/index.html'


class RuleCreateView(generic.TemplateView):
    """Language rule create view."""

    template_name = 'lang/rule/create/index.html'


class RuleDetailView(generic.TemplateView):
    """Language rule detail view."""

    template_name = 'lang/rule/detail/index.html'


class RuleUpdateView(generic.TemplateView):
    """Language rule update view."""

    template_name = 'lang/rule/update/index.html'


class RuleListView(generic.TemplateView):
    """Language rule list view."""

    template_name = 'lang/rule/list/index.html'


class RuleDeleteView(generic.TemplateView):
    """Language rule delete view."""
