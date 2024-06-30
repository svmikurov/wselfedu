Usage
=====

Installation
------------

.. code-block:: console

   $ git clone git@github.com:svmikurov/wselfedu.git
   $ cd wselfedu
   $ pip install poetry
   $ poetry install

Create the database and database user before running the migration.

.. code-block:: console

    $ sudo -u postgres psql

    postgres=# CREATE USER wse_user CREATEDB LOGIN PASSWORD 'wse_pass';
    postgres=# CREATE DATABASE wse_db WITH OWNER wse_user;

Apply migrations

.. code-block:: console

    $ make migrate

Run app
-------

.. code-block:: console

   $ make start
