[![Python CI](https://github.com/svmikurov/wselfedu/actions/workflows/pici.yml/badge.svg)](https://github.com/svmikurov/wselfedu/actions/workflows/pici.yml)  

# Web Self Eduction

Web app for learning English words and multiplication tables.

## Learning English words
When learning an English word, the application provides four levels of knowledge 
of the word. The level of knowledge of a word is determined by the user's actions.
Word knowledge level: study, repeat, check, know.

Read the [documentation](http://localhost:63342/wselfedu/app-wse/docs/build/html/index.html) (local only)  
Read the [documentation](https://svmikurov.github.io/wselfedu/) on GitHub

## Install
Create the database and database user before running the migration.
```
$ sudo -u postgres psql
postgres=# CREATE USER wse_user CREATEDB LOGIN PASSWORD 'wse_pass';
postgres=# CREATE DATABASE wse_db WITH OWNER wse_user;
```