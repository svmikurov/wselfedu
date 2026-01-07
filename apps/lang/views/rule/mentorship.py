"""Language rule view for student."""

from django.views import generic


class RuleStudentView(generic.TemplateView):
    """Language rule student view."""

    template_name = 'lang/rule/detail/student.html'


class RuleStudentListView(generic.TemplateView):
    """Language rule student view."""

    template_name = 'lang/rule/list/student.html'


class RuleMentorListView(generic.TemplateView):
    """Language rule student view."""

    template_name = 'lang/rule/list/mentor.html'
