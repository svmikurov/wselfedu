import os

from django.views.generic import TemplateView
from dotenv import load_dotenv

from english import database as db

load_dotenv()
db_url = os.getenv('DATABASE_URL')


class SqlCategoriesListView(TemplateView):
    """Покажи список категорий, использую запрос SQL с помощью psycopg2."""

    template_name = 'english/cat_list.html'

    connection = db.connect(db_url)
    categories = db.fetch_db_data(connection, db.CATEGORIES_LIST)
    db.close(connection)

    extra_context = {
        'title': 'Список категорий',
        'categories': categories,
    }
