"""Playwright Pytest end-to-end tests.

Uses Page Object Model.

Examples
--------
Simple examples, for more see:
:ref:`Page <pom_page_example>`
:ref:`Test <pom_test_example>`

.. code-block:: python

    class PageClass(POMPage):

        def __init__(self, page: Page) -> None:
            super().__init__(page)
            self.page = page

.. code-block:: python

    import PageClass

    class TestPageClass(POMTest):

        def setUp(self) -> None:
            super().setUp()
            self.test_page = PageClass(self.page)

.. seealso::

    * `Playwright Page Object Model <https://playwright.dev/python/docs/pom>`_
    * `Best Practices <https://playwright.dev/docs/best-practices>`_
    * `playwright-python-tutorial <https://github.com/mxschmitt/playwright-python-tutorial.git>`_
    * `python-django-playwright <https://github.com/mxschmitt/python-django-playwright.git>`_
    * `playwright-python-docker-example <https://github.com/mxschmitt/playwright-python-docker-example.git>`_

"""  # noqa: E501
