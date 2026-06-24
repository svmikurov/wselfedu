# Page Object Model: Django live server & Playwright

## Page example

```python
from .pom.page.base import BasePage

class ExercisePage(BasePage):

    title = 'Home'
    path = '/exercise/'
```

## Test example

```python
from http import HTTPStatus
from playwright.sync_api import expect
from .pom.test.base import BaseTest

class TestExercisePage(BaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.page = ExercisePage(self._page)

    def test_page(self) -> None:
        # Act
        response = self.page.open()

        # Assert
        assert response
        assert response.status == HTTPStatus.OK
        
        expect(self._page).to_have_title(ExercisePage.title)
```

## Run test

```
poetry run pytest
```
