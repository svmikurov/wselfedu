=================
Glossary exercise
=================

Overview
========

Применяется паттерн MVC (Model-View-Controller).

Используемые переменные:
------------------------

- ``lookup_conditions`` : `dict` - словарь условий пользователя для
  формирования задания, хранится в базе данных;
- ``exercise_choices`` : `dict` - словарь возможных выборов содержания условия,
  константа модуля;
- ``exercise_params`` : `dict` - json response сервера, который содержит:
    - ``lookup_conditions``
    - ``exercise_choices``
- ``lookup_parameters`` : `tuple` - кортеж инкапсулированых фильтров запроса к модели,
  формируется контролером при выполнении задания.

Цикл упражнения:
----------------

1. Глоссарий.

Пользователь наполняет коллекцию терминов глоссария.

2. Выборка.

Пользователь выбирает условия фильтрации терминов для изучения,
что в включает в себя цепочку событий:

- пользователь направляет:
    * запрос на выполнение упражнения;
- сервер:
    * вызывает на исполнение соответствующее представление;
    * представление извлекает ``lookup_conditions`` из модели;
    * представление отправляет пользователю ``exercise_params``, который содержит:
        * ``lookup_conditions`` - возможные условия формирования задания;
        * ``exercise_choices`` - список выборов для конкретного условия,
          если условие имеет выбор;
- пользователя направляет:
    * запрос на сохранение измененного ``lookup_conditions`` (необязательно);
    * запрос не выполнение упражнения с неизмененным/измененным ``lookup_conditions``;

    ...

.. note::

    TODO: передать извлечение представлением ``lookup_conditions`` контроллеру

API View (The View MVC)
=======================

Task logic (The Controller MVC)
===============================

.. autoclass:: task.tasks.glossary_exercise.GlossaryExercise
   :members:
   :private-members:

Database queries (The Model MVC)
================================

Constants
---------

.. autodata:: task.orm_queries.glossary_lookup_params.EDGE_PERIODS_TERMS

Query class
-----------

.. autoclass:: task.orm_queries.glossary_lookup_params.GlossaryExerciseLookupParams
   :members:
   :private-members:

The search for terms to complete the task is carried out according to
the criteria contained in the dictionary ``lookup_params``.

Tests
=====

.. automodule:: tests.tests_glossary.test_lookup_term
   :members: