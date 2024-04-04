from loguru import logger

from database.common.db_models import User, QueryResult, db
from database.core import crud

db_delete = crud.delete()


def del_queries(user_id: int) -> None:
    """
    Удаляет лишние записи из таблицы, если они не отображаются в истории поиска.
    В данном случае, последние 10

    :param user_id: id текущего пользователя

    :return: None
    """
    logger.info('Запуск удаления лишних строк')
    cur_user = User.get_or_none(User.user_id == user_id)
    queries = cur_user.queries.order_by(-QueryResult.query_date).limit(10)  # последние 10 запросов
    latest_ids = [line.res_id for line in queries]  # id последних 10 запросов

    all_users_queries = cur_user.queries  # запрос всех результатов пользователя
    all_queries_ids = [line.res_id for line in all_users_queries]  # id всех запросов

    oldest_queries_ids = [q_id for q_id in all_queries_ids if q_id not in latest_ids]  # id запросов пользователя
    # кроме последних 10

    db_delete(db, QueryResult, QueryResult.res_id << oldest_queries_ids)  # запрос на удаление лишнего из таблицы

    logger.info('Завершение удаления')
