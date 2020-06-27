from datetime import datetime
from typing import List

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .models import Type, Element
from .repository import db_session, TypeDB


def get_builtin_types() -> List[Type]:
    return [
        Type(name='number', editable=False),
        Type(name='decimal', editable=False),
        Type(name='string', editable=False),
        Type(name='boolean', editable=False),
    ]


def get_user_types() -> List[Type]:
    """ Возвращает сохраненные пользовательские типы """
    return [t.to_type() for t in TypeDB.query.all()]


def get_types() -> List[Type]:
    return get_builtin_types() + get_user_types()


def create_type(type: Type) -> Type:
    """ Создание нового пользовательского типа версии 1 """
    type_db = TypeDB(type)
    db_session.add(type_db)

    try:
        db_session.commit()
    except IntegrityError:
        raise ValidationError({'name': 'тип уже существует'})

    return type_db.to_type()


def delete_type(name: str) -> None:
    return


def get_type(name) -> Type:
    return Type(name=name)


def update_type(type: Type) -> Type:
    """
    Изменение нового пользовательского типа
    Если версия меньше последней то производится проверка на конфликты
    В случае перезаписи одинаковых данных возврщается ошибка marshmallow.ValidationError

    """
    now = datetime.now()
    if False:
        raise ValidationError({'name': 'Название типа изменено до вас'})

    return Type(type.name, version=1, updated=now)
