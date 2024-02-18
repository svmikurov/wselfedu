import os

from django.views.generic import ListView, TemplateView
from dotenv import load_dotenv

from english import database as db
from english.models import WordModel

load_dotenv()
db_url = os.getenv('DATABASE_URL')


class SqlShowUserWordsView(TemplateView):
    """View user word list page, via SQL queries."""

    template_name = 'english/user_word_list_sql.html'

    sql_request = '''
    SELECT english_wordmodel.id AS pk,
           english_wordmodel.words_eng,
           english_wordmodel.words_rus,
           english_sourcemodel.name AS source,
           english_wordmodel.updated_at AS created_at
    FROM english_wordmodel
    LEFT JOIN english_sourcemodel
    ON english_wordmodel.source_id = english_sourcemodel.id
    LIMIT 19
    '''
    connection = db.connect(db_url)
    words = db.fetch_db_data(connection, sql_request)
    db.close(connection)

    extra_context = {
        'title': 'Мной изучаемые слова (представление SQL)',
        'words': words,
    }


class ShowUserWordsView(ListView):
    """View user word list page, via Django ORM queries."""

    template_name = 'english/user_word_list_sql.html'
    model = WordModel
    context_object_name = 'words'

    def get_queryset(self):
        queryset = super(ShowUserWordsView, self).get_queryset(
        ).select_related(
            'source',
        )[:20]
        return queryset

    extra_context = {
        'title': 'Мной изучаемые слова (представление ORM)',
    }
