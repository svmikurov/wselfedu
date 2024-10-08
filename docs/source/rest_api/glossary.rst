Glossary endpoints
==================

List and Create Glossary endpoint
---------------------------------

.. code-block::

   api/v1/glossary/

+-----------+---------------------------+-------------------------------+
| Method    | Request                   | Response                      |
+===========+===========================+===============================+
| GET       |                           |                               |
+-----------+---------------------------+-------------------------------+
| POST      |                           |                               |
+-----------+---------------------------+-------------------------------+

Glossary Exercise endpoint
--------------------------

.. code-block::

   api/v1/glossary/exercise/

+-----------+---------------------------+-------------------------------+
| Method    | Request                   | Response                      |
+===========+===========================+===============================+
| POST      | * params                  |                               |
|           | * action                  |                               |
|           | * term_id                 |                               |
+-----------+---------------------------+-------------------------------+

Glossary Exercise Parameters endpoint
-------------------------------------

Add or update user Glossary Exercise Parameters.

.. code-block::

   api/v1/glossary/exercise/parameters/

+-----------+-----------------------------------+-------------------------------+
| Method    | Request                           | Response                      |
+===========+===================================+===============================+
| GET       | --                                | HTTP_200_OK                   |
|           |                                   |  * edge_period_items          |
|           |                                   |                               |
|           |                                   |    - alias                    |
|           |                                   |    - humanly                  |
|           |                                   |                               |
|           |                                   |  * categories                 |
|           |                                   |                               |
|           |                                   |    - id                       |
|           |                                   |    - name                     |
|           |                                   |    - url                      |
|           |                                   |    - created_at               |
|           |                                   |    - user                     |
|           |                                   |                               |
|           |                                   |  * parameters                 |
|           |                                   |                               |
|           |                                   |    - period_start_date        |
|           |                                   |    - period_end_date          |
|           |                                   |    - category                 |
|           |                                   |    - progres                  |
|           |                                   |                               |
|           |                                   |  * progres                    |
|           |                                   |                               |
|           |                                   |    - alias                    |
|           |                                   |    - humanly                  |
+-----------+-----------------------------------+-------------------------------+
| POST      | * period_start_date (optional)    | HTTP_200_OK                   |
|           | * period_end_date (optional)      |  * period_start_date          |
|           | * category (optional)             |  * period_end_date            |
|           | * progres (optional)              |  * category                   |
|           |                                   |  * progres                    |
|           |                                   |                               |
|           |                                   | HTTP_201_CREATED              |
|           |                                   |  * period_start_date          |
|           |                                   |  * period_end_date            |
|           |                                   |  * category                   |
|           |                                   |  * progres                    |
|           |                                   |                               |
+-----------+-----------------------------------+-------------------------------+
