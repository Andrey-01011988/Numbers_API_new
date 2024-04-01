from typing import List, Dict, TypeVar, Any

from peewee import ModelSelect

from loguru import logger

from database.common.db_models import BaseModel, db


T = TypeVar('T')


# Операция записи
@logger.catch()
def _store_data(db: db, model: T, *data: List[Dict]) -> None:
    # Защита транзакций средствами ORM:
    # Используем неделимость операций
    with db.atomic():
        # Заменил insert_many, так как из-за особенностей массовой вставки
        # каждая строка должна содержать одни и те же поля
        model.insert(*data).execute()


# Операция чтения
@logger.catch()
def _retrieve_all_data(db: db, model: T, *columns: BaseModel) -> ModelSelect:
    with db.atomic():
        response = model.select(*columns)

    return response


# Операция изменения (update) данных
@logger.catch()
def _update_data(db: db, model: T, *data: Dict) -> None:
    with db.atomic():
        model.update(*data).execute()


# Операция удаления
@logger.catch()
def _delete_data(db:db, model: T, data: Any) -> None:
    """
    Удаляет фрагмент таблицы по уравнению написанному в data
    (выбирается условие по которому будут удалены одна или несколько строк таблицы
    н-р: QueryResult.res_id == 5)

    :param db: б/д
    :param model: таблица
    :param data: уравнение
    :return: None
    """

    with db.atomic():
        model.delete().where(data).execute()


# Фасад
class CRUDInterface:
    @staticmethod
    def create():
        return _store_data

    @staticmethod
    def retrieve():
        return _retrieve_all_data

    @staticmethod
    def update():
        return _update_data

    @staticmethod
    def delete():
        return _delete_data


if __name__ == '__main__':
    _store_data()
    _retrieve_all_data()
    _update_data()
    _delete_data()
    CRUDInterface()
