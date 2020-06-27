from datetime import datetime
from typing import List

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .models import Type, BUILTINS, Element
from .repository import db_session, TypeDB


def get_builtin_types() -> List[Type]:
    return [Type(name=b, editable=False) for b in BUILTINS]


def get_user_types() -> List[Type]:
    """ Возвращает сохраненные пользовательские типы """
    return [t.to_type() for t in TypeDB.query.all()]


def get_types() -> List[Type]:
    return get_builtin_types() + get_user_types()


def _check_types_exists(elements: List[Element]):
    for el in elements or []:
        try:
            get_type(el.type)
        except ValidationError:
            raise ValidationError({'elements': f'для элемента "{el.name}" указан несуществующий тип "{el.type}"'})


def create_type(type: Type) -> Type:
    """ Создание нового пользовательского типа версии 1 """
    if type.is_builtin:
        raise ValidationError({'name': 'имя встроенного типа'})

    _check_types_exists(type.elements)

    type_db = TypeDB(type)
    db_session.add(type_db)

    try:
        db_session.commit()
    except IntegrityError:
        raise ValidationError({'name': 'тип уже существует'})

    return type_db.to_type()


def delete_type(name: str) -> None:
    if name in BUILTINS:
        raise ValidationError({'name': 'нередактируемый тип'})

    type_db = TypeDB.query.filter(TypeDB.name == name).first()
    if not type_db:
        raise ValidationError({'name': 'тип не найден'})

    db_session.delete(type_db)
    db_session.commit()


def get_type(name: str) -> Type:
    if name in BUILTINS:
        return Type(name=name, editable=False)

    type_db = TypeDB.query.filter(TypeDB.name == name).first()
    if not type_db:
        raise ValidationError({'name': 'тип не найден'})

    return type_db.to_type()


def update_type(type: Type) -> Type:
    """
    Изменение нового пользовательского типа
    Если версия меньше последней то производится проверка на конфликты
    В случае перезаписи одинаковых данных возврщается ошибка marshmallow.ValidationError

    """
    _check_types_exists(type.elements)

    now = datetime.now()
    if False:
        raise ValidationError({'name': 'Название типа изменено до вас'})

    return Type(type.name, version=1, updated=now)
