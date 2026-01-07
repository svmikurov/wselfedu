"""Language discipline web urls paths."""

from django.urls import path

from . import views

app_name = 'lang'

urlpatterns = [
    path('', views.IndexLangView.as_view(), name='index'),
    # ----------------------
    # English language rules
    # ----------------------
    path(
        'rule/index/',
        views.RuleIndexView.as_view(),
        name='english_rule_index',
    ),
    path(
        'rule/list/',
        views.RuleListView.as_view(),
        name='english_rule_list',
    ),
    path(
        'rule/create/',
        views.RuleCreateView.as_view(),
        name='english_rule_create',
    ),
    path(  # English language rule for user
        'rule/<int:pk>/detail/',
        views.RuleDetailView.as_view(),
        name='english_rule_detail',
    ),
    path(  # English language rule for students
        'rule/<int:pk>/detail/',
        views.RuleStudentView.as_view(),
        name='english_rule_detail_student',
    ),
    path(
        'rule/<int:pk>/update/',
        views.RuleUpdateView.as_view(),
        name='english_rule_update',
    ),
    path(
        'rule/<int:pk>/delete/',
        views.RuleDeleteView.as_view(),
        name='english_rule_delete',
    ),
    # Rule clause example & exception edit
    path(
        'rule/<int:pk>/edit-example/',
        views.RuleExampleView.as_view(),
        name='english_rule_edit_example',
    ),
    path(
        'rule/<int:pk>/edit-exception/',
        views.RuleExceptionView.as_view(),
        name='english_rule_edit_exception',
    ),
    path(  # Language rule list for mentor
        'rule/list/mentor/',
        views.RuleMentorListView.as_view(),
        name='english_rule_list_mentor',
    ),
    path(  # Language rule list for student
        'rule/list/student/',
        views.RuleStudentListView.as_view(),
        name='english_rule_list_student',
    ),
    # -----------
    # Translation
    # -----------
    path(
        'translation/english/create/',
        views.EnglishTranslationCreateView.as_view(),
        name='translation_english_create',
    ),
    path(
        'translation/english/list/',
        views.EnglishTranslationListView.as_view(),
        name='translation_english_list',
    ),
    path(
        'translation/english/<int:pk>/update/',
        views.EnglishTranslationUpdateView.as_view(),
        name='translation_english_update',
    ),
    path(
        'translation/english/<int:pk>/delete/',
        views.EnglishTranslationDeleteView.as_view(),
        name='translation_english_delete',
    ),
    # -----------------
    # Translation study
    # -----------------
    # - Presentation
    path(
        'translation/english/study/',
        views.EnglishTranslationStudyView.as_view(),
        name='translation_english_study',
    ),
    path(
        'translation/english/study/case/',
        views.EnglishTranslationStudyCaseView.as_view(),
        name='translation_english_study_case',
    ),
    # - Test
    path(
        'translation/english/test/',
        views.TranslationTestView.as_view(),
        name='translation_english_test',
    ),
    path(
        'translation/english/test/progress/',
        views.TranslationTestProgressView.as_view(),
        name='translation_english_test_progress',
    ),
    path(
        'translation/english/test/mentorship/',
        views.TranslationTestMentorshipView.as_view(),
        name='translation_english_test_mentorship',
    ),
    # --------------
    # Study settings
    # --------------
    path(
        'settings/',
        views.study_settings_vew,
        name='settings',
    ),
    # ----
    # Mark
    # ----
    path(
        'mark/create/',
        views.MarkCreateView.as_view(),
        name='mark_create',
    ),
    path(
        'mark/<int:pk>/update/',
        views.MarkUpdateView.as_view(),
        name='mark_update',
    ),
    path(
        'mark/<int:pk>/delete/',
        views.MarkDeleteView.as_view(),
        name='mark_delete',
    ),
    path(
        'mark/<int:pk>/',
        views.MarkDetailView.as_view(),
        name='mark_detail',
    ),
    path(
        'mark/list/',
        views.LabelListView.as_view(),
        name='mark_list',
    ),
]
