Graph
=====

Add relations
-------------

Add relations for `GenericForeignKey` field of `Transaction` model.

.. code-block:: bash
   :caption: bash

   python manage.py graph_models \
           -o temp/graph_models/models.dot \
           --verbose-names \
           --inheritance

.. code-block::
   :caption: models.dot

     ...
     # Add next:

     apps_users_models_transaction_Transaction -> apps_math_models_exercise_MathExercise
     [label="content_object" style="dashed" color="#ff0000"];

     apps_users_models_transaction_Transaction -> apps_foreign_models_exercise_ForeignExercise
     [label="content_object" style="dashed" color="#ff0000"];

   }
   # End file

.. code-block:: bash
   :caption: bash

   dot -Tpng models.dot -o output.png -Granksep=1.5 -Gnodesep=0.5

.. image:: /_static/graph_output.png
