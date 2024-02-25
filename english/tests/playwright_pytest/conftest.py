import pytest


def pytest_addoption(parser):
    """Looks for the `runplaywright` argument"""
    parser.addoption(
        '--runplaywright',
        action='store_true',
        default=False,
        help='run playwright tests',
    )


# Registering marks
# https://docs.pytest.org/en/stable/how-to/mark.html#registering-marks
def pytest_configure(config):
    """Auto-add the slow mark to the config at runtime"""
    config.addinivalue_line(
        'markers', 'playwright: mark test as slow to run'
    )


def pytest_collection_modifyitems(config, items):
    """This skips the tests if runslow is not present"""
    if config.getoption('--runplaywright'):
        # --runplaywright given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason='need --runplaywright option to run')
    for item in items:
        if 'playwright' in item.keywords:
            item.add_marker(skip_slow)


# live_server
# str(live_server)
# live_server + '/foo'
# https://pytest-django.readthedocs.io/en/latest/helpers.html#live-server
@pytest.fixture()
def test_server(page, live_server):
    page.goto(live_server.url)
    return page


# доступ к базе данных для всех моих тестов без маркера django_db
# https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-give-database-access-to-all-my-tests-without-the-django-db-marker
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

# pytest.mark.urls
# settings.ROOT_URLCONF
# https://pytest-django.readthedocs.io/en/latest/helpers.html#pytest-mark-urls-override-the-urlconf

# django_user_model
# settings.AUTH_USER_MODEL
# https://pytest-django.readthedocs.io/en/latest/helpers.html#django-user-model

# manage.py test
# использовать manage.py test с pytest-django
# https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-use-manage-py-test-with-pytest-django

# ожидаемое количество запросов к БД
# 1) django_assert_num_queries
# https://pytest-django.readthedocs.io/en/latest/helpers.html#django-assert-num-queries
# 2) django_assert_max_num_queries
# https://pytest-django.readthedocs.io/en/latest/helpers.html#django-assert-max-num-queries

# ВСЕ ФИКСТУРЫ
# https://github.com/pytest-dev/pytest-django/blob/master/pytest_django/fixtures.py
