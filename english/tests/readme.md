## Описание

Используемая фикстура [wse-fixtures.json](fixtures%2Fwse-fixtures.json) выгружается из базы данных  
`db-wse-fixtures.sqlite3` командой `make create-fixtures`.  
Чтобы получить доступ к базе данных с фикстурами необходимо установить значение  
переменной `DEFAULT_DB=Fixtures` в файле `.env`  

### Имеются следующие экземпляры фикстуры:  
(Внести правки)  
- UserModel: admin, user1;  
- WordModel: word01, word02;  
- SourceModel: source1, source2;  
- CategoryModel: category1, category2;  

### Имеются следующие связи в фикстуре:  
(Внести правки)  
###### knowledge_assessment:  
- admin - word01 : knowledge_assessment = 0;  
- admin - word05 : knowledge_assessment = 0.  
###### WordsFavoritesModel:  
- user1 - word01  


## ToDo

###### Добавить тесты удаления связанных объектов с защитой  
- source;  
- category;  
- ...  

###### test_words.py
- Не содержит тесты на права пользователей

###### Тест Выбери уровень знания слов
- Закончить тест чекбокса "Выбери уровень знания слов" в упражнении "Изучаем слова".  
