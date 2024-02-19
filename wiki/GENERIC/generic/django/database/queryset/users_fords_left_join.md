```cfgrlanguage
SELECT english_wordmodel.id AS pk,
       english_wordmodel.words_eng,
       english_wordmodel.words_rus,
       english_sourcemodel.name AS SOURCE,
       english_wordmodel.updated_at,
       english_worduserknowledgerelation.knowledge_assessment AS assessment,
       english_wordsfavoritesmodel.user_id AS favorite
FROM english_wordmodel
LEFT JOIN english_sourcemodel ON english_wordmodel.source_id = english_sourcemodel.id
LEFT JOIN english_worduserknowledgerelation ON english_wordmodel.id = english_worduserknowledgerelation.word_id
LEFT JOIN english_wordsfavoritesmodel ON english_wordmodel.id = english_wordsfavoritesmodel.word_id
     AND english_wordmodel.user_id = english_wordsfavoritesmodel.user_id
```

```
from django.db.models import F, Q
from english.models import WordModel

WordModel.objects.prefetch_related(
    'knowledge_assessment',
    'favorites',
).filter(
    pk=F('worduserknowledgerelation__word_id')
).annotate(
    # https://stackoverflow.com/questions/10598940/how-to-rename-items-in-values-in-django
    assessment=F('worduserknowledgerelation__knowledge_assessment')
).annotate(
    # FROM english_wordmodel
    # LEFT JOIN english_wordsfavoritesmodel
    # ON  english_wordmodel.id = english_wordsfavoritesmodel.word_id
    # AND english_wordmodel.user_id = english_wordsfavoritesmodel.user_id
    # -------------------------------------------------------------------
    # favorite = условие & условие.
    # условие: Q(поле левой модели = F(поле правой модели))
    # Q - позволяет использовать условие
    # F - позволяет испоьззовать значение поля модели
    favorite=Q(
        pk=F('wordsfavoritesmodel__word_id')
    ) & Q(
        user=F('wordsfavoritesmodel__user_id')
    )
)
```