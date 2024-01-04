[SQLFormat - форматирование отступов запроса](https://sqlformat.org/#result)

С данными в SQL работают с помощью подмножества:  
DML (Data Manipulation Language)

```cfgrlanguage
    INSERT — запрос на вставку данных
    UPDATE — запрос на обновление данных
    DELETE — запрос на удаление данных
```

### Вставка

```cfgrlanguage
INSERT INTO table_name (field1, field2, field3, ...)
VALUES ('value1', 'value2', 10, ...);
```

Вставить сразу 3 записи за 1 запрос:
```cfgrlanguage
INSERT INTO table_name (field1, field2)
VALUES ('Bash', 'bash'),
       ('PHP', 'php'),
       ('Ruby', 'ruby');
```


### Извлечение

Команды выполняются при курсоре:
```cfgrlanguage
db_name=>
```  

Запрос SELECT не является частью DML.
```cfgrlanguage
SELECT * FROM table_name;
```

Запрос с условиями:
```cfgrlanguage
SELECT username,
       created_at
FROM users
WHERE birthday < '2018-10-21'
ORDER BY birthday DESC
LIMIT 2;
```
`ORDER BY` - сортировка  
`ORDER BY birthday DESC` - сортировка в обратномпорядке  
`LIMIT 2` - пангинация  


### Обновление или изменение данных

`WHERE` - проверка на совпадение; сколько совпадений, столько и обновлений  

```cfgrlanguage
UPDATE TABLE_NAME
SET field1 = value2
WHERE field3 = value3;
```
Можно обновить сразу несколько полей
```cfgrlanguage
UPDATE TABLE_NAME
SET field1 = value2,
    field3 = value4
WHERE field5 = value5;
```

```cfgrlanguage
UPDATE TABLE_NAME
SET field1 = value1
WHERE (field2 > 2
       AND field3 < 8)
  OR field4 = value4;
```


### Удаление

```cfgrlanguage
DELETE
FROM TABLE_NAME
WHERE field1 = value1;
```

Очистка таблицы:
```cfgrlanguage
TRUNCATE TABLE_NAME
```