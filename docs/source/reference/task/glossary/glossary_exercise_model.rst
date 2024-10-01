Glossary exercise model
=======================

Constants
---------

.. autodata:: config.constants.EDGE_PERIOD_ARGS
   :no-index:

.. autodata:: config.constants.DEFAULT_GLOSSARY_PARAMS
   :no-index:

.. autodata:: config.constants.EDGE_PERIOD_CHOICES
   :no-index:

.. autodata:: config.constants.PROGRESS_CHOICES
   :no-index:


Queries
-------

The search for terms to complete the task is carried out according to
the criteria contained in the dictionary ``lookup_params``.

.. autoclass:: task.orm_queries.glossary_lookup_params.GlossaryLookupParams
   :members:
   :private-members:
