[Инструкция подключения pgAdmin](https://www.postgresqltutorial.com/postgresql-getting-started/connect-to-postgresql-database/)  
[Как использовать PostgreSQL в приложении Django](https://www.8host.com/blog/kak-ispolzovat-postgresql-v-prilozhenii-django/)  

## Список основных команд  
`...=> \du`             список ролей  
`$ whoami`              имя текущего пользователя  
`$ sudo -u postgres createuser --createdb name` создать роль `name`  

`$ psql -l`             список всех баз данных  
`$ createdb wse`        создать БД `wse`  
`$ dropdb wse`          удалить БД `wse`  

`$ psql wse`            соединится с БД `wse`, `$` -> `wse=>`  
`$ psql postgres`       соединится с БД `postgres`, `$` -> `postgres=>`  

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

