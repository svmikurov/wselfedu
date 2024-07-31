# Generated by Django 4.2.14 on 2024-07-31 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_guardianship'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('english', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MathematicalExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calculation_type', models.CharField(choices=[('add', 'Сложение'), ('sub', 'Вычитание'), ('mul', 'Умножение'), ('div', 'Деление')], max_length=10)),
                ('first_operand', models.PositiveSmallIntegerField()),
                ('second_operand', models.PositiveSmallIntegerField()),
                ('user_solution', models.PositiveSmallIntegerField()),
                ('is_correctly', models.BooleanField(blank=True, null=True)),
                ('solution_time', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('award', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('write_off', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('balance', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('guardianship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.guardianship')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.mathematicalexercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EnglishTaskSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_order', models.CharField(choices=[('RN', 'Перевод в случайном порядке'), ('EN', 'Перевод с английского языка'), ('RU', 'Перевод на английский язык')], default=('RN', 'Перевод в случайном порядке'), max_length=2, verbose_name='Порядок перевода')),
                ('timeout', models.PositiveSmallIntegerField(default=5, verbose_name='Таймаут')),
                ('favorites', models.BooleanField(default=False, verbose_name='Избранное')),
                ('knowledge', models.CharField(choices=[('S', 'Изучаю'), ('R', 'Повторяю'), ('E', 'Проверяю'), ('K', 'Знаю')], default='S', max_length=1, verbose_name='Уровень знания')),
                ('word_count', models.CharField(choices=[('OW', 'Слово'), ('CB', 'Словосочетание'), ('PS', 'Часть предложения'), ('ST', 'Предложение')], default=('OW', 'CB'), max_length=2, verbose_name='Длина выражения')),
                ('date_start', models.CharField(choices=[('DT', 'Сегодня'), ('D3', 'Три дня назад'), ('W1', 'Неделя назад'), ('W2', 'Две недели назад'), ('W3', 'Три недели назад'), ('W4', 'Четыре недели назад'), ('W7', 'Семь недель назад'), ('M3', 'Три месяца назад'), ('M6', 'Шесть месяцев назад'), ('M9', 'Девять месяцев назад'), ('NC', 'Добавлено')], default=('NC', 'Добавлено'), max_length=2, verbose_name='Добавлено после')),
                ('date_end', models.CharField(choices=[('DT', 'Сегодня'), ('D3', 'Три дня назад'), ('W1', 'Неделя назад'), ('W2', 'Две недели назад'), ('W3', 'Три недели назад'), ('W4', 'Четыре недели назад'), ('W7', 'Семь недель назад'), ('M3', 'Три месяца назад'), ('M6', 'Шесть месяцев назад'), ('M9', 'Девять месяцев назад')], default=('DT', 'Сегодня'), max_length=2, verbose_name='Добавлено до')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='english.categorymodel', verbose_name='Категория')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='english.sourcemodel', verbose_name='Источник')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Настройки "Изучаем слова"',
                'verbose_name_plural': 'Настройки "Изучаем слова"',
            },
        ),
    ]
