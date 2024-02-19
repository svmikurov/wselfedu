Экспорт в читаемый вид только таблицы `usersbalanceupbyday` из `users.models`
```cfgrlanguage
./manage.py dumpdata english.vocabularywordsmodel --indent 2 > db_.json
```

Экспорт без уникальных таблиц для ПК:
```cfgrlanguage
./manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db.json
```

Импорт:
```cfgrlanguage
./manage.py loaddata db.json
```