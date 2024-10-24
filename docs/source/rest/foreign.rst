Learning foreign words API endpoints
====================================

Attributes:

    * "count"    - foreign word count in dictionary
    * "next"     - link to next pagination page
    * "previous" - link to previous pagination page
    * "results"  - list of word mapping, its elements has attributes:
        - "id"       - word ID
        - "foreign_word" - word by foreign
        - "native_word" - word by native

    {required fild} - "foreign_word" or "native_word"

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
|           | * native_word                 |  * id                         |
|           |                               |  * foreign_word               |
|           |                               |  * native_word                |
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
|           |                               |  * native_word                |
+-----------+-------------------------------+-------------------------------+
| PUT       | * foreign_word                | HTTP_200_OK                   |
|           | * native_word                 |  * id                         |
|           |                               |  * foreign_word               |
|           |                               |  * native_word                |
|           |                               |                               |
|           |                               | HTTP_400_BAD_REQUEST          |
|           |                               |  * {required fild}            |
+-----------+-------------------------------+-------------------------------+
| PATCH     | * foreign_word (optionally)   | HTTP_200_OK                   |
|           | * native_word  (optionally)   |  * id                         |
|           |                               |  * foreign_word               |
|           |                               |  * native_word                |
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
|           |                               |      * categories:            |
|           |                               |          * alias              |
|           |                               |          * humanly            |
|           |                               |      * progress:              |
|           |                               |          * alias              |
|           |                               |          * humanly            |
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

+-----------+----------------------------------+----------------------------+
| Method    | Request                          | Response                   |
+===========+==================================+============================+
| POST      | * period_start_date (optionally) | HTTP_200_OK                |
|           | * period_end_date (optionally)   |  * id                      |
|           | * category (optionally)          |  * question_text           |
|           | * progress (optionally)          |  * answer_text             |
|           |                                  |  * items                   |
|           |                                  |  * assessment              |
+-----------+----------------------------------+----------------------------+

View: :py:func:`foreign.views.rest.exercise.translate_exercise`.

Fields:
    Request:
        - ``period_start_date`` -- start of period of adding word to study,
          choice alias only from :obj:`~config.constants.EDGE_PERIOD_CHOICES` (`str`);
        - ``period_end_date`` -- end of period of adding word to study,
          choice alias only from :obj:`~config.constants.EDGE_PERIOD_CHOICES` (`str`);
        - ``category`` -- word category ID (`None` | `int`);
        - ``progress`` -- progress of word study,
          choice from :obj:`~config.constants.PROGRESS_CHOICES` (`str`);

    Response:
        - ``id`` -- word ID (`int`);
        - ``question_text`` -- word to translate (`str`);
        - ``answer_text`` -- translate of word (`str`);
        - ``items`` -- count of words to choice for exercise,
          by selected exercise parameters (`int`);
        - ``assessment`` -- words study assessment (`int`);

Example:

.. code-block::
   :caption: Request:

        {
            "period_start_date": "NC",
            "period_end_date": "DT",
            "progress": "S"
        }

.. code-block::
   :caption: Response:

        {
            "id": 15,
            "question_text": "tweezers",
            "answer_text": "пинцет",
            "items": 10,
            "assessment": 7
        }
