Glossary exercise overview
==========================

Применяется паттерн MVC (Model-View-Controller).

Используемые переменные:
------------------------

- ``lookup_conditions`` : `dict` - словарь условий пользователя для
  формирования задания, хранится в базе данных (необязательно),
  модель :obj:`~glossary.models.GlossaryExerciseParams`;
- ``exercise_choices`` : `dict` - словарь возможного выбора для условий:
    - для фильтрации по датам - :py:data:`~config.constants.EDGE_PERIOD_CHOICES`;
    - для фильтрации по прогрессу изучения - :py:data:`~config.constants.PROGRES_CHOICES`;
    - для фильтрации по категории :obj:`~glossary.models.GlossaryCategory`;
    - имеет значения по умолчанию :py:data:`~config.constants.DEFAULT_GLOSSARY_PARAMS`.

.. _exercise_params:

- ``exercise_params`` : `dict` - json response сервера с параметрами упражнения:
    see also:
      - :py:data:`~config.constants.EDGE_PERIOD_ALIASES`
      - :py:data:`~config.constants.PROGRES_ALIASES`

    .. code-block:: python

       exercise_params = {
            'lookup_conditions': lookup_conditions,
            'exercise_choices': {
                'edge_period_items': EDGE_PERIOD_ALIASES,
                'categories': categories,
                'progres': PROGRES_ALIASES,
            },
       }

- ``lookup_parameters`` : `tuple[Q, ...]` - кортеж инкапсулированых фильтров запроса к модели,
  формируется контролером при выполнении задания.

Цикл упражнения:
----------------

1. Глоссарий
^^^^^^^^^^^^

Пользователь наполняет коллекцию терминов глоссария.

2. Выборка
^^^^^^^^^^

Пользователь выбирает условия фильтрации терминов для изучения, при
выполнении упражнения, что в включает в себя цепочку событий:

- пользователь:
    * отправляет запрос
      (:ref:`GET request path <rest_api/glossary:Glossary Exercise Parameters endpoint>`)
      на получение параметров по умолчанию;
- сервер, представление :py:meth:`~task.views.exercise_glossary_views.glossary_exercise_parameters`:
    * извлекает ``lookup_conditions`` из базы данных, model
      :py:class:`~glossary.models.GlossaryExerciseParams`;
    * отправляет пользователю `exercise_params`_:
- пользователь:
    * отправляет запрос
      (:ref:`POST request path <rest_api/glossary:Glossary Exercise Parameters endpoint>`)
      на сохранение измененного ``lookup_conditions`` (необязательно);
    * отправляет запрос
      (:ref:`POST request path <rest_api/glossary:Glossary Exercise endpoint>`)
      на выполнение упражнения с неизмененными/измененными параметрами ``lookup_conditions``.
- сервер:
    * представление
      :py:meth:`~task.views.exercise_glossary_views.glossary_exercise_parameters`
      выполняет запрос на сохранение измененных параметров ``lookup_conditions`` (необязательно);
    * представление создает ``exercise`` - экземпляр
      :py:class:`~task.tasks.glossary_exercise.GlossaryExercise`
      (контроллера) и передает ему ``lookup_conditions``;
    * представление через свойство ``task_data`` экземпляра получает
      данные задачи и отправляет их пользователю.
- ...

.. todo:

   - обработка ответа пользователя
        - следующая задача
        - знаю / не знаю
        - ``lookup_conditions`` - приходят от клиента

   Думаю этого будет пока достаточно, потом надо подключить редис,
   для интернет версии.
