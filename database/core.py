from database.utils.CRUD import CRUDInterface
from database.common.db_models import db, BaseModel

# коннект
db.connect()

# Создание таблиц на основе класса BaseModel
db.create_tables(BaseModel.__subclasses__())

# Выдача интерфейса
crud = CRUDInterface()

if __name__ == '__main__':
    crud()
