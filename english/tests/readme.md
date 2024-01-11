Используемая фикстура [wse-fixtures.json](fixtures%2Fwse-fixtures.json) 
выгружается из базы данных для фикстуры.  
Чтобы получить доступ к базе данных с фикстурами необходимо установить
следующее значение переменной `DEFAULT_DB=Fixtures` в файле `.env`

Имеются следующие экземпляры:
    - UserModel: admin, user1;
    - WordModel: word01, word02;
    - SourceModel: source1, source2;
    - CategoryModel: category1, category2;

Имеются следующие отношения('word - user (assessment)'):
    - WordUserKnowledgeRelation:
        - word01 - admin (0);
        - word02 - admin (0)
    - WordsFavoritesModel:
        - word01 - user1.

"""ToDo"""

Добавить тесты удаления связанных объектов с защитой
    - source;  
    - category;  
    - ...  

Исправить тест test_update_words_knowledge_assessment_view.py:  
    - тестирует вью обновить статус избрано/не избрано слово;  
!   - не выполняется редирект;  
    - подумать о вынесении в отдельные тесты:  
        - тестирование вью;  
        - тестирование функции обновления статуса.  