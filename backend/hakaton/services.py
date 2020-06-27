from typing import List
from datetime import datetime
from .models import Type


def get_builtin_types() -> List[Type]:
    return [
        Type(name='number'),
        Type(name='decimal'),
        Type(name='string'),
        Type(name='boolean'),
    ]


def get_user_types() -> List[Type]:
    """ Возвращает сохраненные пользовательские типы """
    return []


def get_types() -> List[Type]:
    return get_builtin_types() + get_user_types()


def create_type(type: Type) -> Type:
    """ Создание нового пользовательского типа версии 1 """
    now = datetime.now()

    return Type(type.name, version=1, updated=now)


def delete_type(name: str) -> None:
    return


def get_type(name) -> Type:
    return Type(name=name)


def update_type(type: Type) -> Type:
    """
    Изменение нового пользовательского типа
    Если версия меньше последней то производится проверка на конфликты
    В случае перезаписи одинаковых данных возврщается ошибка
    """
    now = datetime.now()

    return Type(type.name, version=1, updated=now)
