from datetime import datetime
from typing import List

from marshmallow import ValidationError

from .models import Type, Element


def get_builtin_types() -> List[Type]:
    return [
        Type(name='number', editable=False),
        Type(name='decimal', editable=False),
        Type(name='string', editable=False),
        Type(name='boolean', editable=False),
    ]


def get_user_types() -> List[Type]:
    """ Возвращает сохраненные пользовательские типы """
    return [
        Type(
            name='Person',
            elements=[
                Element(name='firstName', type='string'),
                Element(name='lastName', type='string'),
                Element(name='middleName', type='string'),
                Element(name='Age', type='integer'),
            ],
            version=1,
            updated=datetime.now(),
        ),
    ]


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
    В случае перезаписи одинаковых данных возврщается ошибка marshmallow.ValidationError

    """
    now = datetime.now()
    if False:
        raise ValidationError({'name': 'Название типа изменено до вас'})
    
    return Type(type.name, version=1, updated=now)
