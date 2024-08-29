English-Russian dictionary endpoints
====================================

Attributes:

    * "count"    - word count in dictionary
    * "next"     - link to next pagination page
    * "previous" - link to previous pagination page
    * "results"  - list of word mapping, its elements has attributes:
        - "id"       - word ID
        - "word_eng" - word by english
        - "word_rus" - word by russian

    {required fild} - "word_eng" or "word_rus"

Word List, Create endpoints
---------------------------

.. code-block::

   /api/v1/word/

+----------------------+----------------------------+-------------------------------+
| Method               | Request                    | Response                      |
+======================+============================+===============================+
| GET                  | --                         | HTTP_200_OK                   |
|                      |                            |  * count                      |
|                      |                            |  * next                       |
|                      |                            |  * previous                   |
|                      |                            |  * results                    |
+----------------------+----------------------------+-------------------------------+
| POST                 | * word_eng                 | HTTP_200_OK                   |
|                      | * word_eng                 |  * id                         |
|                      |                            |  * word_eng                   |
|                      |                            |  * word_eng                   |
|                      |                            |                               |
|                      |                            | HTTP_400_BAD_REQUEST          |
|                      |                            |  * {required fild}            |
+----------------------+----------------------------+-------------------------------+

Word Retrieve, Update, Destroy endpoints
----------------------------------------

.. code-block::

   /api/v1/word/id/

+----------------------+----------------------------+-------------------------------+
| Method               | Request                    | Response                      |
+======================+============================+===============================+
| GET                  | --                         | HTTP_200_OK                   |
|                      |                            |  * id                         |
|                      |                            |  * word_eng                   |
|                      |                            |  * word_rus                   |
+----------------------+----------------------------+-------------------------------+
| PUT                  | * word_eng                 | HTTP_200_OK                   |
|                      | * word_rus                 |  * id                         |
|                      |                            |  * word_eng                   |
|                      |                            |  * word_rus                   |
|                      |                            |                               |
|                      |                            | HTTP_400_BAD_REQUEST          |
|                      |                            |  * {required fild}            |
+----------------------+----------------------------+-------------------------------+
| PATCH                | * word_eng (optionally)    | HTTP_200_OK                   |
|                      | * word_rus (optionally)    |  * id                         |
|                      |                            |  * word_eng                   |
|                      |                            |  * word_rus                   |
+----------------------+----------------------------+-------------------------------+
| DELETE               |                            | HTTP_204_NO_CONTENT           |
+----------------------+----------------------------+-------------------------------+

