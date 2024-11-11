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
|           |                                 |    * source                   |
|           |                                 |    * progres                  |
|           |                                 |    * count_first              |
|           |                                 |    * count_last               |
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

Example, GET method::

    {
        "lookup_conditions": {
            "period_start_date": "NC",
            "period_end_date": "DT",
            "progress": "S",
            "category": null,
            "source": null,
            "count_first": 0,
            "count_last": 0
        },
        "exercise_choices": {
            "edge_period_items": [
                {
                    "alias": "DT",
                    "humanly": "Сегодня"
                },
                {
                    "alias": "D3",
                    "humanly": "Три дня назад"
                },
                {
                    "alias": "W1",
                    "humanly": "Неделя назад"
                },
                {
                    "alias": "W2",
                    "humanly": "Две недели назад"
                },
                {
                    "alias": "W3",
                    "humanly": "Три недели назад"
                },
                {
                    "alias": "W4",
                    "humanly": "Четыре недели назад"
                },
                {
                    "alias": "W7",
                    "humanly": "Семь недель назад"
                },
                {
                    "alias": "M3",
                    "humanly": "Три месяца назад"
                },
                {
                    "alias": "M6",
                    "humanly": "Шесть месяцев назад"
                },
                {
                    "alias": "M9",
                    "humanly": "Девять месяцев назад"
                },
                {
                    "alias": "NC",
                    "humanly": "Добавлено"
                }
            ],
            "categories": [
                {
                    "alias": 2,
                    "humanly": "GitHub Actions"
                },
                {
                    "alias": 1,
                    "humanly": "PostgreSQL"
                },
                {
                    "alias": null,
                    "humanly": "Не выбрано"
                }
            ],
            "progress": [
                {
                    "alias": "S",
                    "humanly": "Изучаю"
                },
                {
                    "alias": "R",
                    "humanly": "Повторяю"
                },
                {
                    "alias": "E",
                    "humanly": "Проверяю"
                },
                {
                    "alias": "K",
                    "humanly": "Знаю"
                }
            ]
        }
    }

Glossary progress endpoint
--------------------------

.. code-block::

   api/v1/glossary/progress/

+-----------+---------------------------------+-------------------------------+
| Method    | Request                         | Response                      |
+===========+=================================+===============================+
| POST      | * action                        | HTTP_204_OK                   |
|           | * id                            |                               |
+-----------+---------------------------------+-------------------------------+

Where:
    - ``'action'`` -- ``'know'`` or ``'not_know'``, user assessment of
      knowledge of the term;
    - ``'id'`` -- term ID.


Category
--------

Where:
    - ``'count'`` -- count of categories;
    - ``'next'`` -- pagination next url;
    - ``'previous'`` -- pagination previous url;
    - ``'results'`` -- list of categories;
    - ``'alias'`` -- category ID;
    - ``'humanly'`` -- category name.

.. code-block::

   api/v1/glossary/category/

View: :py:class:`~glossary.views.glossary.GlossaryListCreateAPIView`

+-----------+---------------------------------+-------------------------------+
| Method    | Request                         | Response                      |
+===========+=================================+===============================+
| GET       | --                              | HTTP_200_OK                   |
|           |                                 |  * count                      |
|           |                                 |  * next                       |
|           |                                 |  * previous                   |
|           |                                 |  * results:                   |
|           |                                 |     * alias                   |
|           |                                 |     * humanly                 |
+-----------+---------------------------------+-------------------------------+
| POST      | * humanly                       | HTTP_201_CREATED              |
|           |                                 |  * alias                      |
|           |                                 |  * humanly                    |
+-----------+---------------------------------+-------------------------------+

.. code-block::

   api/v1/glossary/category/{id}/

View: :py:class:`~glossary.views.glossary.GlossaryDetailAPIView`

+-----------+---------------------------------+-------------------------------+
| Method    | Request                         | Response                      |
+===========+=================================+===============================+
| GET       | --                              | HTTP_200_OK                   |
|           |                                 |  * alias                      |
|           |                                 |  * humanly                    |
+-----------+---------------------------------+-------------------------------+
| PUT       | * humanly                       | HTTP_200_OK                   |
|           |                                 |  * alias                      |
|           |                                 |  * humanly                    |
+-----------+---------------------------------+-------------------------------+
| DELETE    | --                              | HTTP_204_NO_CONTENT           |
+-----------+---------------------------------+-------------------------------+
