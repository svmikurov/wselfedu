Glossary exercise overview
==========================

Variables used
--------------

.. glossary::

   lookup_conditions
      ``lookup_conditions`` : `dict` - словарь условий пользователя для
      формирования задания, хранится в базе данных (необязательно),
      модель :obj:`~glossary.models.GlossaryExerciseParams`;

   exercise_choices
      ``exercise_choices`` : `dict` - словарь возможного выбора для условий:
      - для фильтрации по датам - :py:data:`~config.constants.EDGE_PERIOD_CHOICES`;
      - для фильтрации по прогрессу изучения - :py:data:`~config.constants.PROGRESS_CHOICES`;
      - для фильтрации по категории :obj:`~glossary.models.GlossaryCategory`;
      - имеет значения по умолчанию :py:data:`~config.constants.DEFAULT_GLOSSARY_PARAMS`.

   exercise_params
      ``exercise_params`` : `dict` - json response сервера с параметрами упражнения.

      see also:
         - :py:data:`~config.constants.EDGE_PERIOD_ALIASES`
         - :py:data:`~config.constants.PROGRESS_ALIASES`
         - Glossary exercise parameters :ref:`endpoint <rest/glossary:Glossary Exercise Parameters endpoint>`
           on GET request method response.

      .. code-block:: python

         exercise_params = {
             'lookup_conditions': lookup_conditions,
             'exercise_choices': {
                 'edge_period_items': EDGE_PERIOD_ALIASES,
                 'categories': categories,
                 'progress': PROGRESS_ALIASES,
             },
         }

   lookup_parameters
      ``lookup_parameters`` : `tuple[Q, ...]` - кортеж инкапсулированых фильтров запроса к модели,
      формируется контролером при выполнении задания.

Цикл упражнения:
----------------

Пользователь наполняет коллекцию терминов глоссария.

Пользователь выбирает условия фильтрации терминов для изучения, при
выполнении упражнения, что в включает в себя цепочку событий:

- пользователь:
    * отправляет запрос (:ref:`GET request params <rest/glossary:Glossary Exercise Parameters endpoint>`)
      на получение параметров упражнения по умолчанию;
- сервер, представление :py:meth:`~task.views.glossary_exercise_drf_views.glossary_exercise_parameters`:
    * извлекает ``lookup_conditions`` из базы данных, model :py:class:`~glossary.models.GlossaryExerciseParams`;
    * отправляет пользователю :term:`exercise_params`:
- пользователь:
    * отправляет запрос (:ref:`POST request params <rest/glossary:Glossary Exercise Parameters endpoint>`)
      на сохранение измененного ``lookup_conditions`` (необязательно);
- сервер, представление :py:meth:`~task.views.glossary_exercise_drf_views.glossary_exercise_parameters`:
    * выполняет запрос на сохранение измененных параметров ``lookup_conditions`` (необязательно);
- пользователь:
    * отправляет запрос (:ref:`POST request exercise <rest/glossary:Glossary Exercise endpoint>`)
      на выполнение упражнения, передает неизмененные/измененные параметры ``lookup_conditions``
      для текущего упражнения.
- сервер, представление :py:meth:`~task.views.glossary_exercise_drf_views.glossary_exercise`:
    * создает ``exercise`` - экземпляр :py:class:`~task.tasks.glossary_exercise.GlossaryExercise`
      и передает ему ``lookup_conditions``;
    * представление через свойство ``task_data`` экземпляра получает данные задачи и отправляет их пользователю,
      see: :ref:`Glossary Exercise endpoint Response <rest/glossary:Glossary Exercise endpoint>`.
- пользователь:
    * отмечает ``"знаю"`` / ``"не знаю"`` значение термина (необязательно), оправляя запрос на
      :ref:`POST request progress <rest/glossary:Glossary progress endpoint>`;
    * отправляет запрос на новое задание
      (:ref:`POST request exercise <rest/glossary:Glossary Exercise endpoint>`).
- сервер:
    * представление :py:meth:`~glossary.views_drf.update_term_study_progres`
      сохраняет обновленный прогресс изучения в базе данных;
    * возвращает новое задание.
- в цикле выполнения упражнения:
    * пользователь отправляет запрос ``"знаю"`` / ``"не знаю"`` (необязательно);
    * пользователь отправляет запрос на новое задание;
    * сервер обновляет прогресс изучения термина (необязательно);
    * возвращает новое задание.
