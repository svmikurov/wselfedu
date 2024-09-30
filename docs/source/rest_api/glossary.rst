Glossary endpoints
==================

List and Create Glossary endpoint
---------------------------------

.. code-block::

   api/v1/glossary/

+-----------+---------------------------------+-------------------------------+
| Method    | Request                         | Response                      |
+===========+=================================+===============================+
| GET       |                                 |                               |
+-----------+---------------------------------+-------------------------------+
| POST      |                                 |                               |
+-----------+---------------------------------+-------------------------------+

Glossary Exercise endpoint
--------------------------

.. code-block::

   api/v1/glossary/exercise/

+-----------+---------------------------------+-------------------------------+
| Method    | Request                         | Response                      |
+===========+=================================+===============================+
| POST      | - lookup_conditions:            | HTTP_200_OK                   |
|           |                                 |   * id                        |
|           |   * period_start_date           |   * question_text             |
|           |   * period_end_date             |   * answer_text               |
|           |   * category                    |                               |
|           |   * progres                     | HTTP_400_BAD_REQUEST          |
|           |                                 |   * {fild}                    |
+-----------+---------------------------------+-------------------------------+

Glossary Exercise Parameters endpoint
-------------------------------------

Add or update user Glossary Exercise Parameters.

.. code-block::

   api/v1/glossary/exercise/parameters/

+-----------+---------------------------------+-------------------------------+
| Method    | Request                         | Response                      |
+===========+=================================+===============================+
| GET       | --                              | HTTP_200_OK                   |
|           |                                 |  - lookup_conditions:         |
|           |                                 |                               |
|           |                                 |    * period_start_date        |
|           |                                 |    * period_end_date          |
|           |                                 |    * category                 |
|           |                                 |    * progres                  |
|           |                                 |                               |
|           |                                 |  - exercise_choices:          |
|           |                                 |                               |
|           |                                 |    - edge_period_items:       |
|           |                                 |                               |
|           |                                 |      * alias                  |
|           |                                 |      * humanly                |
|           |                                 |                               |
|           |                                 |    - categories:              |
|           |                                 |                               |
|           |                                 |      * id                     |
|           |                                 |      * name                   |
|           |                                 |      * url                    |
|           |                                 |      * created_at             |
|           |                                 |      * user                   |
|           |                                 |                               |
|           |                                 |    - progres:                 |
|           |                                 |                               |
|           |                                 |      * alias                  |
|           |                                 |      * humanly                |
+-----------+---------------------------------+-------------------------------+
| POST      | * period_start_date (optional)  | HTTP_200_OK                   |
|           | * period_end_date (optional)    |  * period_start_date          |
|           | * category (optional)           |  * period_end_date            |
|           | * progres (optional)            |  * category                   |
|           |                                 |  * progres                    |
|           |                                 |                               |
|           |                                 | HTTP_201_CREATED              |
|           |                                 |  * period_start_date          |
|           |                                 |  * period_end_date            |
|           |                                 |  * category                   |
|           |                                 |  * progres                    |
|           |                                 |                               |
|           |                                 | HTTP_400_BAD_REQUEST          |
|           |                                 |  * {fild}                     |
+-----------+---------------------------------+-------------------------------+
