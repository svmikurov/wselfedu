#################
Production deploy
#################

.. _production_deploy:

Clone repo:

.. code-block:: console
   :caption: bash:

   git clone git@github.com:svmikurov/wselfedu.git

Go to project:

.. code-block:: console
   :caption: bash:

   cd wselfedu/

Add .env and .env.postgres:

.. code-block:: console
   :caption: bash:

   cp .env.example .env && \
   cp .env.postgres.example .env.postgres

Add to ``.env`` and ``.env.postgres`` values to replace the empty values
in the example below, or leave the default values.
Value POSTGRES_DB is POSTGRES_NAME value.

.. code-block:: console
   :caption: bash:

   nano .env

.. code-block:: console
   :caption: .env

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

   nano .env.postgres

.. code-block:: console
   :caption: .env.postgres

   POSTGRES_DB=
   POSTGRES_USER=
   POSTGRES_PASSWORD=

Build and Up Docker:

.. code-block:: console
   :caption: bash:

    make up

Make migrations:

.. code-block:: console
   :caption: bash:

   make migrate

Make collectstatic

.. code-block:: console
   :caption: bash:

   make collectstatic

Uncomment ``username`` in Dockerfile.prod and run application:

.. code-block:: console
   :caption: bash:

   make down

.. code-block:: console
   :caption: bash:

   nano ./docker/project/Dockerfile.prod

.. code-block:: console
   :caption: ./docker/project/Dockerfile.prod

   ...
   RUN adduser --disabled-password app-user
   USER app-user
   ...

.. code-block:: console
   :caption: bash:

   make build

.. code-block:: console
   :caption: bash:

   make up

This is all.
