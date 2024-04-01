from datetime import datetime

import peewee

db = peewee.SqliteDatabase('requests_history.db')


# TODO решил сделать две реляционные таблицы для пользователей и их сообщений
# Базовая модель
class BaseModel(peewee.Model):
    created_at = peewee.DateField(default=datetime.now())

    class Meta:
        database = db


class User(BaseModel):
    """
    Модель пользователя

    user_id: первичный ключ модели, будет совпадать с Telegram ID.
    Это значит, что он будет уникальным для всей таблицы

    username: никнейм в Telegram. Может быть не указан

    first_name: имя в Telegram. Может быть не указано

    last_name: фамилия в Telegram. Может быть не указана
    """
    user_id = peewee.IntegerField(primary_key=True)
    username = peewee.CharField(null=True)
    first_name = peewee.CharField(null=True)
    last_name = peewee.CharField(null=True)


class QueryResult(BaseModel):
    """
    Модель результатов пользовательских запросов

    res_id: ID результата. AutoField показывает, что это первичный ключ,
    а значение будет автоматически увеличиваться на единицу. Аналог
    PRIMARY KEY AUTOINCREMENT

    user: внешний ключ, ссылающийся на пользователя.backref создаёт
    обратную ссылку: мы сможем получить задачи пользователя с помощью user.queries

    query_date: дата запроса

    result_text: текст ответа на запрос
    """
    res_id = peewee.AutoField()
    user = peewee.ForeignKeyField(User, backref="queries")
    query_date = peewee.DateTimeField()
    result_text = peewee.TextField()

    def __str__(self):
        return f'{self.res_id} - {self.result_text} - создан: {self.query_date}'



