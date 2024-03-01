# https://pytest-django.readthedocs.io/en/latest/database.html#database-access
```
pytestmark = pytest.mark.django_db		# доступ к БД всем тестам модуля

@pytest.mark.django_db				# доступ к БД всем тестам класса
class TestUsers:
    pytestmark = pytest.mark.django_db		# доступ к БД методу
    def test_my_user(self):
        me = User.objects.get(username='me')
        assert me.is_superuser
```