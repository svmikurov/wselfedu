# Ветки git

## Создание ветки

#### Создать ветку `edu_branch`:
```cfgrlanguage
git branch edu_branch
```

#### Посмотреть существующие ветки:
```cfgrlanguage
$ git branch
  edu_branch
* main
```

#### Создать ветку `edu_branch` и сразу переключится на нее:
Используем команду `checkout` и ее флаг `-b`
```
git checkout -b edu_branch
```


## Переключение между ветками

Переключится на ветку `edu_branch`:
```cfgrlanguage
git checkout edu_branch
```
```cfgrlanguage
$ git branch
* edu_branch
  main
```


## Отправить в репозиторий изменение отдельной ветки
Отправим ветку `main`:
```cfgrlanguage
git push origin main
```


## Слияние

### Добавить изменения в основную ветку

Рекомендуемый способ: слить ветку разработки с main (основной),  
после внесения изменений в основной
```cfgrlanguage
git merge main
```
Cлить ветку <branchname> с текущей веткой,  
для этого перейти на нужную ветку.
```cfgrlanguage
git merge <branchname>
```
Только если я один работаю с ветками.
```cfgrlanguage
git rebase main 
```

### Обновить ветку edu_branch до main:
Находясь в своей ветке:
- если эта ветка только наша и над ней работаем только мы:
```cfgrlanguage
git rebase master
```
- либо загружаем с сервера:
```cfgrlanguage
git pull --rebase origin/main
```
Если есть конфликты, то:
- правим их и выполняем:
```cfgrlanguage
git add <конфликтующие_файлы>
```
- затем:
```cfgrlanguage
git rebase --continue
```
- не забудь про миграции:
```cfgrlanguage
make migrate
```