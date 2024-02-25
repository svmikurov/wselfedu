"""
Test home page not logged in site visitor and logged-in user.

    Run test page with "/".


Run:
    # without make start
    $ pytest -v english/tests/playwright_pytest/test_home_page_mark.py --runplaywright --headed --slowmo 1000
where:
    pytest      # run pytest
    -v          # display path/fail::func_name [100%] instead of dots ...
    --runplaywright     # run the marked tests by @pytest.mark.playwright()
    --headed            # execute with on page pause of 1000 milliseconds
"""
import pytest
from playwright.sync_api import expect

from english.tests.playwright.pw_framework import is_role_visible
from users.models import UserModel

HOME_URL = 'http://127.0.0.1:8000/'
"""Home page URL.
"""

# Enabling database access in tests
# https://pytest-django.readthedocs.io/en/latest/database.html#enabling-database-access-in-tests
# Включение доступа к базе данных всех тестов
pytestmark = pytest.mark.django_db

# @pytest.mark.playwright()
# def test_get_page_status(test_server):
#     """Test home page status 200."""
#     expect(test_server).to_be_ok()


@pytest.mark.playwright()
def test_home_page_navbar(test_server):
    """Test basic navbar."""
    is_role_visible(test_server, 'link', 'WSE')
    expect(test_server.get_by_role('link', name='Английский язык')).to_be_visible()
    expect(test_server.get_by_role('link', name='Регистрация')).to_be_visible()
    expect(test_server.get_by_role('link', name='Войти')).to_be_visible()


@pytest.mark.playwright()
def test_nome_page_body(test_server):
    """Тест кнопки перехода на упражнение Изучаем слова."""
    expect(test_server.get_by_text('Домашняя страница')).to_be_visible()
    is_role_visible(test_server, 'button', 'Упражнение "Изучаем слова"')
    is_role_visible(test_server, 'button', 'Добавить слово в словарь')

    test_server.get_by_role('button', name='Изучаем слова').click()
    expect(test_server.get_by_text('Изучаем слова')).to_be_visible()


# Enabling database access in tests
# https://pytest-django.readthedocs.io/en/latest/database.html#enabling-database-access-in-tests
# @pytest.mark.django_db
# Включение доступа к базе данных только этого теста
def test_my_user():
    UserModel.objects.create_superuser(username='admin')
    me = UserModel.objects.get(username='admin')
    assert me.is_superuser


# rf - RequestFactory
# https://pytest-django.readthedocs.io/en/latest/helpers.html#rf-requestfactory
# from myapp.views import my_view
#
# def test_details(rf, admin_user):
#     request = rf.get('/customer/details')
#     # Remember that when using RequestFactory, the request does not pass
#     # through middleware. If your view expects fields such as request.user
#     # to be set, you need to set them explicitly.
#     # The following line sets request.user to an admin user.
#     request.user = admin_user
#     response = my_view(request)
#     assert response.status_code == 200

# client - django.test.Client
# https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
def test_with_client(client):
    response = client.get('/')
    assert response.status_code == 200
