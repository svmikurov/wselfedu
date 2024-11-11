#######
Install
#######

.. code-block:: console
   :caption: Clone repo:

   git clone git@github.com:svmikurov/wselfedu.git

.. code-block:: console
   :caption: Go to project:

   cd wselfedu/

Add environments:

.. code-block:: console
   :caption: Copy :

   cp .env_vars/.env.example           .env_vars/.env && \
   cp .env_vars/.env.postgres.example  .env_vars/.env.postgres && \
   cp .env_vars/.env.wse.example       .env_vars/.env.wse

In the ``.env`` and ``.env.postgres`` files fill the empty values
of example below or leave the default values.
Value ``POSTGRES_DB`` is ``POSTGRES_NAME`` value.

.. code-block:: console
   :caption: bash:

   nano .env_vars/.env

.. code-block:: console
   :caption: .env_vars/.env

   SECRET_KEY=
   DEBUG=0
   ENVIRONMENT=production

   # Database settings
   POSTGRES_NAME=
   POSTGRES_USER=
   POSTGRES_PASS=
   POSTGRES_HOST=wse-db-postgres
   POSTGRES_PORT=5432

.. code-block:: console
   :caption: bash:

   nano .env_vars/.env.postgres

.. code-block:: console
   :caption: .env_vars/.env.postgres

   POSTGRES_DB=
   POSTGRES_USER=
   POSTGRES_PASSWORD=

Build and Up Docker:

.. code-block:: console
   :caption: bash:

   make build up

Make migrations:

.. code-block:: console
   :caption: bash:

   make migrate

Make collectstatic:

.. code-block:: console
   :caption: bash:

   make collectstatic

Create superuser

.. code-block:: console
   :caption: bash:

   make createsuperuser


Development
===========

   nano .env_vars/.env

.. code-block:: console
   :caption: .env_vars/.env

   DEBUG=1
   ENVIRONMENT=development

Run tests:

.. code-block:: console
   :caption: bash:

   make check


Possible problems
=================

.. code-block:: console
   :caption: If you already have TCP port 0.0.0.0:80 occupied, you can free it

   systemctl stop apache2
