=================
Glossary exercise
=================

Overview
========


Task class
==========

.. autoclass:: task.tasks.glossary_exercise.GlossaryExercise
   :members:
   :private-members:

Database queries
================

Constants
---------

.. autodata:: task.orm_queries.glossary_lookup_params.EDGE_PERIODS_TERMS

.. autoclass:: task.orm_queries.glossary_lookup_params.GlossaryExerciseLookupParams
   :members:
   :private-members:

The search for terms to complete the task is carried out according to
the criteria contained in the dictionary ``lookup_params``.

Tests
=====

.. automodule:: tests.tests_glossary.test_lookup_term
   :members: