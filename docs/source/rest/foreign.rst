Learning foreign words API endpoints
====================================

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
|           |                               |  * results:                   |
|           |                               |     * id                      |
|           |                               |     * foreign_word            |
|           |                               |     * native_word             |
+-----------+-------------------------------+-------------------------------+
| POST      | * foreign_word                | HTTP_201_CREATED              |
|           | * native_word                 |  * id                         |
|           |                               |  * foreign_word               |
|           |                               |  * native_word                |
|           |                               |                               |
|           |                               | HTTP_400_BAD_REQUEST          |
|           |                               |  * {required fild}            |
+-----------+-------------------------------+-------------------------------+

Fields:
 - ``count`` -- foreign word count in dictionary (`int`);
 - ``next`` -- link to next pagination page (`str`);
 - ``previous`` -- link to previous pagination page (`str`);
 - ``results`` -- list of word mapping, its elements has attributes (`dict`);
 - ``id`` -- word ID (`int`);
 - ``foreign_word`` -- word by foreign (`str`);
 - ``native_word`` -- word by native (`str`).

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

Fields:
 - ``id`` -- word ID (`int`);
 - ``foreign_word`` -- word by foreign (`str`);
 - ``native_word`` -- word by native (`str`).

Exercise params
---------------

Endpoint to get or update the exercise parameters.

.. code-block::

   /api/v1/foreign/params/

+-----------+-------------------------------+-------------------------------+
| Method    | Request                       | Response                      |
+===========+===============================+===============================+
| GET       | --                            | HTTP_200_OK                   |
|           |                               |  * lookup_conditions:         |
|           |                               |     * order                   |
|           |                               |     * timeout                 |
|           |                               |     * favorites               |
|           |                               |     * progress                |
|           |                               |     * word_count              |
|           |                               |     * period_start_date       |
|           |                               |     * period_end_date         |
|           |                               |     * count_first             |
|           |                               |     * count_last              |
|           |                               |     * category                |
|           |                               |     * source                  |
|           |                               |  * exercise_choices:          |
|           |                               |     * edge_period_items:      |
|           |                               |        * alias                |
|           |                               |        * humanly              |
|           |                               |     * categories:             |
|           |                               |        * alias                |
|           |                               |        * humanly              |
|           |                               |     * progress:               |
|           |                               |        * alias                |
|           |                               |        * humanly              |
+-----------+-------------------------------+-------------------------------+
| PUT       | * order                       | HTTP_201_CREATED              |
|           | * timeout                     |  * order                      |
|           | * favorites                   |  * timeout                    |
|           | * progress                    |  * favorites                  |
|           | * word_count                  |  * progress                   |
|           | * period_start_date           |  * word_count                 |
|           | * period_end_date             |  * period_start_date          |
|           | * count_first                 |  * period_end_date            |
|           | * count_last                  |  * count_first                |
|           | * category                    |  * count_last                 |
|           | * source                      |  * category                   |
|           |                               |  * source                     |
|           |                               |                               |
|           |                               | HTTP_204_NO_CONTENT           |
+-----------+-------------------------------+-------------------------------+

View: :py:func:`~foreign.views.rest.exercise.params_view`.

Serializer :py:class:`~foreign.serializers.ExerciseChoiceSerializer`

See: :term:`lookup_conditions`, :term:`exercise_choices`.

Fields:
 - ``order`` -- the order in which language translations
   of words are displayed (`str`), choice alias only from
   :obj:`~config.constants.LANGUAGE_ORDER_CHOICE`;
 - ``timeout`` -- show the learning word time, sec (`int`);
 - ``favorites`` --will be display only favorites words if `True`,
   all otherwise (`bool`);
 - ``progress`` -- progress of word study, choice alias only from
   :obj:`~config.constants.PROGRESS_CHOICES` (`str`);
 - ``word_count`` -- length of verbal expression (`list[str]`),
   choice alias only from :obj:`~config.constants.WORD_COUNT_CHOICE`;
 - ``period_start_date`` -- start of period of adding word to study,
   choice alias only from :obj:`~config.constants.EDGE_PERIOD_CHOICES` (`str`);
 - ``period_end_date`` -- end of period of adding word to study,
   choice alias only from :obj:`~config.constants.EDGE_PERIOD_CHOICES` (`str`);
 - ``count_first`` -- count of first added words (`int`);
 - ``count_last`` -- count of last added words (`int`).
 - ``category`` -- word category ID (`int`);
 - ``source`` -- word source ID (`int`);

Example:

.. code-block::
   :caption: Request:

    {
        "order": "TR",
        "timeout": 5,
        "favorites": false,
        "progress": "K",
        "word_count": [
            "OW",
            "CB"
        ],
        "period_start_date": "NC",
        "period_end_date": "DT",
        "count_first": 0,
        "count_last": 0,
        "category": null,
        "source": null
    }


Exercise
--------

Endpoint to get task data.

.. code-block::

   /api/v1/foreign/exercise/

+-----------+----------------------------------+----------------------------+
| Method    | Request                          | Response                   |
+===========+==================================+============================+
| POST      | * order (optionally)             | HTTP_200_OK                |
|           | * favorites (optionally)         |  * id                      |
|           | * category (optionally)          |  * question_text           |
|           | * source (optionally)            |  * answer_text             |
|           | * progress (optionally)          |  * item_count              |
|           | * word_count (optionally)        |  * assessment              |
|           | * period_start_date (optionally) |                            |
|           | * period_end_date (optionally)   | HTTP_204_NO_CONTENT        |
|           | * count_first (optionally)       |  * details                 |
|           | * count_last (optionally)        |                            |
+-----------+----------------------------------+----------------------------+

View: :py:func:`~foreign.views.rest.exercise.exercise_view`.

Serializer for request: :py:class:`~foreign.serializers.ExerciseParamSerializer`.

Serializer for response: :py:class:`~foreign.serializers.ExerciseSerializer`.

Returns status 204 if no words were found for study according to the given parameters.

Fields:
    Request:
        - ``order`` -- the order in which language translations
          of words are displayed (`str`), choice alias only from
          :obj:`~config.constants.LANGUAGE_ORDER_CHOICE`;
        - ``favorites`` --will be display only favorites words if `True`,
          all otherwise (`bool`);
        - ``category`` -- word category ID (`int`);
        - ``source`` -- word source ID (`int`);
        - ``progress`` -- progress of word study, choice alias only from
          :obj:`~config.constants.PROGRESS_CHOICES` (`str`);
        - ``word_count`` -- length of verbal expression (`list[str]`),
          choice alias only from :obj:`~config.constants.WORD_COUNT_CHOICE`;
        - ``period_start_date`` -- start of period of adding word to study,
          choice alias only from :obj:`~config.constants.EDGE_PERIOD_CHOICES` (`str`);
        - ``period_end_date`` -- end of period of adding word to study,
          choice alias only from :obj:`~config.constants.EDGE_PERIOD_CHOICES` (`str`);
        - ``count_first`` -- count of first added words (`int`);
        - ``count_last`` -- count of last added words (`int`).

    Response:
        - ``id`` -- word ID (`int`);
        - ``question_text`` -- word to translate (`str`);
        - ``answer_text`` -- translate of word (`str`);
        - ``item_count`` -- count of words to choice for exercise,
          by selected exercise parameters (`int`);
        - ``assessment`` -- words study assessment (`int`);
        - ``details`` -- message (`int`).

Example:

.. code-block::
   :caption: Request:

        {
            "order": "TR",
            "favorites": true,
            "category": 2,
            "source": 2,
            "progress": "S",
            "word_count": ["OW"],
            "period_start_date": "NC",
            "period_end_date": "DT",
            "count_first": 100,
            "count_last": 0,
        }

.. code-block::
   :caption: Response:

        {
            "id": 15,
            "question_text": "tweezers",
            "answer_text": "пинцет",
            "item_count": 10,
            "assessment": 7
        }

Assessment
----------

Endpoint to update the word knowledge assessment.

.. code-block::

   /api/v1/foreign/assessment/

+-----------+-------------------------------+-------------------------------+
| Method    | Request                       | Response                      |
+===========+===============================+===============================+
| POST      | * item_id                     | HTTP_204_NO_CONTENT           |
|           | * action                      |                               |
|           |                               | HTTP_400_BAD_REQUEST          |
|           |                               |  * {field}                    |
|           |                               |  * {non_field_errors}         |
+-----------+-------------------------------+-------------------------------+

View: :py:func:`~foreign.views.rest.exercise.update_word_assessment_view`.

Serializer: :py:class:`~foreign.serializers.WordAssessmentSerializer`.

Fields:
 - ``item_id`` -- word ID (`int`);
 - ``action`` -- assessment action (`str`), ``'know'`` or ``'not_know'``.

Example:

.. code-block::
   :caption: Request:

        {
            "item_id": 7,
            "action": "know",
        }
