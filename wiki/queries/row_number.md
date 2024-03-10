```def get_queryset(self):
    """Get a queryset with only user words.

    Add `row_number` to instance of queryset.
    Add a category and source of word to queryset.
    """
    queryset = super(WordListView, self).get_queryset(
    ).select_related(
        'category',
        'source',
    ).filter(
        user=self.request.user
    ).order_by(
        '-pk',
    ).annotate(
        # https://stackoverflow.com/questions/68500663/how-to-annotate-a-queryset-adding-row-numbers-groupped-by-a-field
        row_number=Window(
            # https://docs.djangoproject.com/en/5.0/ref/models/database-functions/#rownumber
            expression=RowNumber(),
            order_by=[F('pk')]
        )
    )
    return queryset
```