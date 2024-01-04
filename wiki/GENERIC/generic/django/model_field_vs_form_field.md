## Model fields
has:  
    - field option (параметры) (max_length, ...)  
    - field type (CharField, ...)

## Form fields
has:  
    - field "Core field arguments" (аргументы основного поля) (max_length, ...)  
    - field type (CharField, ...)

[django code](https://github.com/django/django/blob/14917c9ae272f47d23401100faa6cefa8e1728bf/django/forms/fields.py#L99C18-L99C18)

```cfgrlanguage
    def __init__(
        self,
        *,
        required=True,
        widget=None,
        label=None,
        ...
    ):
```
`(self, *, ...)` - * означает, что передаются **ТОЛЬКО** именованные аргументы

### Методы класса формы