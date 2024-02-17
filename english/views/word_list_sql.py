from django.db import connection
from django.views.generic import TemplateView


sql_request = '''
SELECT *
FROM english_wordmodel
LIMIT 10
'''


def my_custom_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()

    return row


class SqlWordListView(TemplateView):
    """Покажи список слов, использую запрос SQL с помощью psycopg2."""

    template_name = 'english/word_list_sql.html'

    words = my_custom_sql(sql_request)
    extra_context = {
        'title': 'Список слов',
        'words': words,
    }
