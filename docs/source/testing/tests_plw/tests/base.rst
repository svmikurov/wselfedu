Base Test
=========

Usage
-----

Inherit your test classes from POMTest.

.. code-block:: python

    from tests_plw.tests.base import POMTest

    class TestClass(POMTest):

    def setUp(self) -> None:
        super().setUp()
        self.test_page = PageClass(self.page)
        self.user = self.create_user(username='User')
        self.authorize_test_page(user=self.user)
        self.page_path = f'/users/profile/{self.user.pk}'
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

Create a user if necessary::

    self.user = self.create_user(username='User')

Authorize the user::

    self.authorize_test_page(user=self.user)

Specify the path to the page::

    self.page_path = f'/users/profile/{self.user.pk}'

Navigate to page, use page instance method
:py:meth:`navigate <tests_plw.pages.base.BasePage.navigate>`::

    self.test_page.navigate(page_url=self.page_url)

Content
-------

.. automodule:: tests_plw.tests.base

POMTest attribute:
    - :py:attr:`user <UserMixin.user>` (optionally)
    - :py:attr:`page_path <BaseTest.page_path>`

POMTest methods:
    - :py:meth:`create_user <UserMixin.create_user>`
    - :py:meth:`authorize_test_page <UserMixin.authorize_test_page>`

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
