DB schema with Dj migrations
============================

Create empty migration
----------------------

1. Create empty migration with ``create_custom_schema`` name into ``main`` app

.. code-block:: bash
   :caption: bash


   $ python manage.py makemigrations --empty main --name create_custom_schema
   Migrations for 'main':
   ../main/migrations/0001_create_custom_schema.py

Django will create a migration module

.. code-block:: python
   :caption: ../main/migrations/0001_create_custom_schema.py

   from django.db import migrations

   class Migration(migrations.Migration):

       dependencies = [
       ]

       operations = [
       ]

2. Add the field value ``db_table = 'main"."mymodel'`` to the model metadata

.. code-block:: python

   class MyModel(models.Model):
      ...
       class Meta:
           db_table = 'main"."mymodel'
           ...

3. Add sql code

.. code-block:: python
   :caption: ../main/migrations/0001_create_custom_schema.py

   from django.db import migrations
   from django.db.backends.base.schema import BaseDatabaseSchemaEditor
   from django.apps.registry import Apps

   def create_schema(
       apps: Apps,
       schema_editor: BaseDatabaseSchemaEditor
   ) -> None:
       schema_editor.execute("""
           -- Schema for main app tables
           CREATE SCHEMA main;
           GRANT ALL PRIVILEGES ON SCHEMA main TO db_user;
           ALTER SCHEMA main OWNER TO db_user;
       """)

   class Migration(migrations.Migration):
      ...

4. If you need to run the migration before the standard migrations, add

.. code-block:: python
   :caption: ../main/migrations/0001_create_custom_schema.py

      class Migration(migrations.Migration):

         run_before = [
             ('contenttypes', '0001_initial'),
         ]
         ...

5. Make migrations

.. code-block:: bash
   :caption: bash

   $ python manage.py makemigrations
   Migrations for 'main':
     ../main/migrations/0002_initial.py
       + Create model MyModel

.. code-block:: bash
   :caption: ../main/migrations/

   0001_create_custom_schema.py
   0002_initial.py

Migrations will add a ``dependency`` on creating a custom schema

.. code-block:: python
   :caption: ../main/migrations/0002_initial.py

      class Migration(migrations.Migration):

          initial = True

          dependencies = [
              ('main', '0001_create_custom_schema'),
          ]
          ...

6. Check with terminal ``psql`` the schema ``main`` and the creation of the model ``MyModel``

.. code-block:: bash
   :caption: psql

   db_name=# \dn
            Список схем
      Имя    |     Владелец
   ----------+-------------------
    main     | db_user
    public   | pg_database_owner
    ...
   (... строк)

.. code-block:: bash
   :caption: psql

   db_name=# \dt main.*
                Список отношений
    Схема |     Имя     |   Тип   | Владелец
   -------+-------------+---------+----------
    main  | mymodel     | таблица | db_user
