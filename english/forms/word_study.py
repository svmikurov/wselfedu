from django import forms

WORD_STUDY_STAGE_CHOICE = [
    ('AL', 'Все'),  # all
    ('WS', 'Изучение'),  # word study
    ('CK', 'Повторение'),  # consolidation of knowledge
    ('CH', 'Проверка'),  # check of knowledge
]
KNOWLEDGE_STAGE_LEVELS = {
    'AL': {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
    'WS': {0, 1, 2, 3, 4, 5},
    'CK': {6, 7, 8},
    'CH': {9, 10},
}


class WordStudyStageChoiceForm(forms.Form):
    word_study_stage = forms.ChoiceField(
        choices=WORD_STUDY_STAGE_CHOICE,
        select='WS',
    )


def get_level_study(stage_choice: str) -> set:
    return KNOWLEDGE_STAGE_LEVELS[stage_choice]
