[Инструкция подключения pgAdmin](https://www.postgresqltutorial.com/postgresql-getting-started/connect-to-postgresql-database/)  
[Как использовать PostgreSQL в приложении Django](https://www.8host.com/blog/kak-ispolzovat-postgresql-v-prilozhenii-django/)  

## Список основных команд  

`$ psql db_name -c "\du"` подменяет `db_name=> \du` 

`--`                    выделение комментария  
`...=> \du`             список ролей  
`$ psql wse -c "\du"`   список ролей
`$ whoami`              имя текущего пользователя  
`$ sudo -u postgres createuser --createdb name` создать роль `name`  
```cfgrlanguage
Задать пароль для пользователя
$ sudo -u postgres psql
postgres=# ALTER ROLE {user_name} PASSWORD '{password}';
```

`$ psql -l`             список всех баз данных  
`$ createdb wse`        создать БД `wse`  
`$ dropdb wse`          удалить БД `wse`  
`postgres=> CREATE DATABASE wse;`   создать БД `wse`  
`postgres=> DROP DATABASE wse;`     удалить БД `wse`  

`$ psql postgres`       соединится с БД `postgres`, `$` -> `postgres=>`  
`$ psql wse`            соединится с БД `wse`, `$` -> `wse=>`  

`...=> \q`              выход, `...=>` в `$`  


## Работа с БД

### Создание роли пользователя.

Создайте роль `name`, запускать от пользователя `postgres`.  
Флаг `--createdb` добавляет роли возможность создавать базы данных, 
по умолчанию этой возможности нет.
```cfgrlanguage
sudo -u postgres createuser --createdb name
```

Посмотреть список ролей, команда `\du` (Describe Users).
```cfgrlanguage
postgres=> \du
```
выведет
```
                                   List of roles
 Role name |                         Attributes                         | Member of 
-----------+------------------------------------------------------------+-----------
 dev       | Create DB                                                  | {}
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

postgres=>
```


### Создание базы данных в СУБД  

команда
```cfgrlanguage
createdb
```
Опция `--owner` позволяет указать владельца создаваемой базы данных  


## Создание таблиц  

[CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)  
[Типы данных](https://postgrespro.ru/docs/postgresql/15/datatype)  
[Онлайн-песочница для выполнения SQL-запросов](https://www.db-fiddle.com/)  

```cfgrlanguage
CREATE TABLE table_name (
    name            varchar(255),
    slug            varchar(255),
    lessons_count   integer,
    body            text,
);
```
### Типы полей
```
`varchar(255)`      строка ограниченной переменной длины  
`text`              строка неограниченной переменной длины  
`integer`           типичный выбор для целых чисел  
`bigint`            целое в большом диапазоне  
`timestamp`      	дата и время (без часового пояса)  
`date`           	дата (без времени суток)  
`time`              время суток (без даты)  

`boolean`           TRUE, 't', 'true', 'y', 'yes', 'on', '1'  
                    FALSE, 'f', 'false', 'n', 'no', 'off', '0'  

`NULL`
```

`...=> \d`              список таблиц базы данных `...`  
`...=> \dt`             список всех таблиц базы данных `...`  
`...=> \d table_name`   структура таблицы `table_name`  

`...=> DROP TABLE table_name`   удалить таблицу `table_name`  

### ОШИБКИ

1) Ошибка, что не выбрана база данных.  
Невозможно соединиться с СУБД, если не указать конкретную базу данных. 
Ее можно указать самостоятельно — передать один аргумент в `psql`.
```cfgrlanguage
$ psql
psql: FATAL:  database "dev" does not exist
```
Решение:
```cfgrlanguage
$ psql postgres
postgres=>
```

