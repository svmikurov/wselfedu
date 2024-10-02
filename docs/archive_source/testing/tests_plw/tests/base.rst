Base Test
=========

Usage
-----

Inherit your test classes from POMTest.

.. code-block:: python
   :caption: Test default user profile page:

    from tests_plw.tests.base import POMTest

    class TestClass(POMTest):

    def setUp(self) -> None:
        super().setUp()
        self.test_page = PageClass(self.page)
        self.authorize_test_page()
        self.page_path = self.test_page.path.format(self.user.pk)
        self.test_page.navigate(page_url=self.page_url)

    def test_odo_ne(self) -> None:
        self.test_page.do_one()
        expect(self.text_page.locator_one).to_have_text('one')

    def test_do_two(self) -> None:
        self.test_page.do_two()
        expect(self.text_page.locator_two).to_have_text('two')

Let’s go through this example:

Create test page instance::

    self.test_page = PageClass(self.page)

Authorize the default user::

    self.authorize_test_page()

Specify the path to the page::

    self.page_path = self.test_page.path.format(self.user.pk)

Navigate to page, uses page instance method
:py:meth:`navigate <tests_plw.pages.base.BasePage.navigate>`::

    self.test_page.navigate(page_url=self.page_url)

Brief overview
--------------

.. automodule:: tests_plw.tests.base

POMTest :ref:`testing/tests_plw/tests/base:Fixture`:
    - :py:attr:`BaseTest.page <BaseTest.page>`
    - :py:meth:`BaseTest.run_around_tests <BaseTest.run_around_tests>`

POMTest class derived attributes:
    - :py:attr:`BaseTest.page_url <BaseTest.page_url>`
    - :py:attr:`BaseTest.page_host <BaseTest.page_host>`
    - :py:attr:`BaseTest.page_path <BaseTest.page_path>`
    - :py:attr:`UserMixin.user <UserMixin.user>` (optionally)
    - :py:attr:`UserMixin.username <UserMixin.username>`
    - :py:attr:`UserMixin.password <UserMixin.password>`

POMTest class derived methods:
    - :py:meth:`BaseTest.setUpClass <BaseTest.setUpClass>`
    - :py:meth:`UserMixin.create_user <UserMixin.create_user>`
    - :py:meth:`UserMixin.authorize_test_page <UserMixin.authorize_test_page>`

.. seealso::

    * `StaticLiveServerTestCase <https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#specialized-test-case-to-support-live-testing>`_

Reference
---------

.. autoclass:: tests_plw.tests.base.BaseTest
   :members:

.. autoclass:: tests_plw.tests.base.UserMixin
   :members:

.. autoclass:: tests_plw.tests.base.POMTest
   :members:

Fixture
-------

.. literalinclude:: ../../../../../tests_plw/tests/base.py
   :pyobject: BaseTest.run_around_tests
