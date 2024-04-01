```cfgrlanguage
    def get_queryset(self):
        """Get user word list with relations.
        """
        favorite_user = WordModel.objects.filter(
            wordsfavoritesmodel__word_id=F('pk'),
            wordsfavoritesmodel__user_id=self.request.user
        ).values('pk')

        queryset = super().get_queryset(
        ).select_related(
            'source',
        ).prefetch_related(
            'knowledge_assessment',
        ).filter(
            user=self.request.user
        ).filter(
            # `worduserknowledgerelation__user_id__isnull=True` allows
            # to a create query using LEFT JOIN
            Q(worduserknowledgerelation__user_id__isnull=True)
            | Q(worduserknowledgerelation__user_id=self.request.user.pk)
        ).annotate(
            assessment=F('worduserknowledgerelation__knowledge_assessment'),
        ).annotate(
            # if `favorite` is `True` then word is favorites
            favorite=Q(pk__in=favorite_user)
        )
        
        return queryset
```

```cfgrlanguage
SELECT "english_wordmodel"."id",
       "english_wordmodel"."user_id",
       "english_wordmodel"."words_eng",
       "english_wordmodel"."words_rus",
       "english_wordmodel"."source_id",
       "english_wordmodel"."category_id",
       "english_wordmodel"."word_count",
       "english_wordmodel"."created_at",
       "english_wordmodel"."updated_at",
       "english_worduserknowledgerelation"."knowledge_assessment" AS "assessment",
       "english_wordmodel"."id" IN
  (SELECT U0."id"
   FROM "english_wordmodel" U0
   INNER JOIN "english_wordsfavoritesmodel" U1 ON (U0."id" = U1."word_id")
   WHERE (U1."user_id" = 2
          AND U1."word_id" = (U0."id"))) AS "favorite",
       "english_sourcemodel"."id",
       "english_sourcemodel"."name",
       "english_sourcemodel"."user_id",
       "english_sourcemodel"."url",
       "english_sourcemodel"."description",
       "english_sourcemodel"."created_at",
       "english_sourcemodel"."updated_at"
FROM "english_wordmodel"
LEFT OUTER JOIN "english_worduserknowledgerelation" ON ("english_wordmodel"."id" = "english_worduserknowledgerelation"."word_id")
LEFT OUTER JOIN "english_sourcemodel" ON ("english_wordmodel"."source_id" = "english_sourcemodel"."id")
WHERE ("english_wordmodel"."user_id" = 2
       AND ("english_worduserknowledgerelation"."user_id" IS NULL
            OR "english_worduserknowledgerelation"."user_id" = 2))
ORDER BY "english_wordmodel"."id" ASC
```