#### Проверить наличие прав администратора
[@staff_member_required](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#the-staff-member-required-decorator)
```cfgrlanguage
@staff_member_required
def my_view(reauest)
    ...
```

#### Проверить вошел ли пользователь в систему
[@login_required](https://docs.djangoproject.com/en/5.0/topics/auth/default/#the-login-required-decorator)
```cfgrlanguage
@login_required
def my_view(request):
    ...
```