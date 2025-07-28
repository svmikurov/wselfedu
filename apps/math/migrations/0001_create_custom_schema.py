from django.apps.registry import Apps
from django.db import migrations, connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

from utils.load import get_db_user


def create_schema(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
    """Create schema."""
    db_user = get_db_user()
    quoted_user = connection.ops.quote_name(db_user)

    sql = f"""
    CREATE SCHEMA IF NOT EXISTS math;
    GRANT ALL PRIVILEGES ON SCHEMA math TO {quoted_user};
    ALTER SCHEMA math OWNER TO {quoted_user};
    """

    schema_editor.execute(sql)


def reverse_schema(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
    """Create reverse schema."""
    schema_editor.execute('DROP SCHEMA IF EXISTS math CASCADE;')


class Migration(migrations.Migration):
    run_before = [
        ('contenttypes', '0001_initial'),
    ]

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_schema, reverse_schema)
    ]
