Learning foreign words API endpoints
====================================

Attributes:

    * "count"    - foreign word count in dictionary
    * "next"     - link to next pagination page
    * "previous" - link to previous pagination page
    * "results"  - list of word mapping, its elements has attributes:
        - "id"       - word ID
        - "foreign_word" - word by foreign
        - "russian_word" - word by russian

    {required fild} - "foreign_word" or "russian_word"

Word List, Create endpoints
---------------------------

.. code-block::

   /api/v1/foreign/

+-----------+-------------------------------+-------------------------------+
| Method    | Request                       | Response                      |
+===========+===============================+===============================+
| GET       | --                            | HTTP_200_OK                   |
|           |                               |  * count                      |
|           |                               |  * next                       |
|           |                               |  * previous                   |
|           |                               |  * results                    |
+-----------+-------------------------------+-------------------------------+
| POST      | * foreign_word                | HTTP_201_CREATED              |
|           | * russian_word                |  * id                         |
|           |                               |  * foreign_word               |
|           |                               |  * russian_word               |
|           |                               |                               |
|           |                               | HTTP_400_BAD_REQUEST          |
|           |                               |  * {required fild}            |
+-----------+-------------------------------+-------------------------------+

Word Retrieve, Update, Destroy endpoints
----------------------------------------

.. code-block::

   /api/v1/foreign/id/

+-----------+-------------------------------+-------------------------------+
| Method    | Request                       | Response                      |
+===========+===============================+===============================+
| GET       | --                            | HTTP_200_OK                   |
|           |                               |  * id                         |
|           |                               |  * foreign_word               |
|           |                               |  * russian_word               |
+-----------+-------------------------------+-------------------------------+
| PUT       | * foreign_word                | HTTP_200_OK                   |
|           | * russian_word                |  * id                         |
|           |                               |  * foreign_word               |
|           |                               |  * russian_word               |
|           |                               |                               |
|           |                               | HTTP_400_BAD_REQUEST          |
|           |                               |  * {required fild}            |
+-----------+-------------------------------+-------------------------------+
| PATCH     | * foreign_word (optionally)   | HTTP_200_OK                   |
|           | * russian_word (optionally)   |  * id                         |
|           |                               |  * foreign_word               |
|           |                               |  * russian_word               |
+-----------+-------------------------------+-------------------------------+
| DELETE    |                               | HTTP_204_NO_CONTENT           |
+-----------+-------------------------------+-------------------------------+

Exercise params
---------------

.. code-block::

   /api/v1/foreign/params/

+-----------+-------------------------------+-------------------------------+
| Method    | Request                       | Response                      |
+===========+===============================+===============================+
| GET       | --                            | HTTP_200_OK                   |
|           |                               |  * lookup_conditions:         |
|           |                               |      * period_start_date      |
|           |                               |      * period_end_date        |
|           |                               |      * category               |
|           |                               |      * progress               |
|           |                               |  * exercise_choices:          |
|           |                               |      * edge_period_items:     |
|           |                               |          * alias              |
|           |                               |          * humanly            |
|           |                               |  * categories:                |
|           |                               |      * {}                     |
|           |                               |  * progress:                  |
|           |                               |      * alias                  |
|           |                               |      * humanly                |
+-----------+-------------------------------+-------------------------------+
| POST      | --                            | HTTP_201_OK                   |
+-----------+-------------------------------+-------------------------------+

The :py:func:`foreign.views.rest.exercise.exercise_parameters` view.
Saves the POST payload to :py:class:`foreign.models.params.TranslateParams`, see it fields.

See also: :term:`lookup_conditions`, :term:`exercise_choices`.

Exercise
--------

.. code-block::

   /api/v1/foreign/exercise/

+-----------+-------------------------------+-------------------------------+
| Method    | Request                       | Response                      |
+===========+===============================+===============================+
|           | --                            | HTTP_200_OK                   |
|           |                               |  *                            |
|           |                               |  *                            |
|           |                               |  *                            |
+-----------+-------------------------------+-------------------------------+

The :py:func:`foreign.views.rest.exercise.translate_exercise` view.
