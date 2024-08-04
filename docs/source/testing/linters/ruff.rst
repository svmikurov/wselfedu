====
ruff
====

.. note::

   Documentation is awaiting completion.

`Tutorial <https://docs.astral.sh/ruff/tutorial/#tutorial>`_

`The settings by default <https://docs.astral.sh/ruff/configuration/>`_

.. code-block:: console

   ruff check

`Fix safety <https://docs.astral.sh/ruff/linter/#fix-safety>`_

.. code-block:: console

   ruff check --fix

.. code-block:: console

   ruff check path/ --select B010

.. code-block:: console

   ruff check path/ --select B010 --fix

.. code-block:: console

   ruff format --diff

.. code-block:: console

   ruff format

.. code-block:: console

   ruff check --watch

Rule
""""

Select rule to check

.. code-block:: console

   ruff check path/ --select I001

.. code-block:: console

   ruff rule F821

Error suppression
"""""""""""""""""

`Error suppression <https://docs.astral.sh/ruff/linter/#error-suppression>`_

.. code-block:: console
   :caption: example:

   # ruff: noqa: F841
