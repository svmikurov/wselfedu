"""Language discipline web urls paths."""

from django.urls import path

from . import views

app_name = 'lang'

urlpatterns = [
    path('', views.IndexLangView.as_view(), name='index'),
    # -----------------~~~~~~~~~~~~~~~~
    # English language study mentorship
    # -----------------~~~~~~~~~~~~~~~~
    path(
        'rule/<int:pk>/assignment/create/',
        views.RuleAssignmentCreate.as_view(),
        name='english_rule_assignment_create',
    ),
    # ----------------------
    # English language rules
    # ----------------------
    path(
        'rule/',
        views.RuleIndexView.as_view(),
        name='english_rule',
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
    path(
        'rule/<int:pk>/detail/',
        views.RuleDetailView.as_view(),
        name='english_rule_detail',
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
        'rule/<int:pk>/clause/create/',
        views.ClauseCreateView.as_view(),
        name='english_clause_create',
    ),
    path(
        'rule/<int:pk>/clause/update/',
        views.ClauseUpdateView.as_view(),
        name='english_clause_update',
    ),
    path(
        'rule/<int:pk>/add-word-example/',
        views.WordExampleAddView.as_view(),
        name='english_example_word_add',
    ),
    path(
        'rule/<int:pk>/add-task-example/',
        views.TaskExampleAddView.as_view(),
        name='english_example_task_add',
    ),
    path(
        'rule/<int:pk>/add-exception/',
        views.ExceptionAddView.as_view(),
        name='english_exception_add',
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
