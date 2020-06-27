from datetime import datetime
from typing import Dict, List, Tuple

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .models import Diff, Type, BUILTINS, Element
from .repository import db_session, TypeDB
from .schemas import DiffSchema, TypeSchema


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

    type_db = _get_db_type(name)
    db_session.delete(type_db)
    db_session.commit()


def get_type(name: str) -> Type:
    if name in BUILTINS:
        return Type(name=name, editable=False)

    return _get_db_type(name).to_type()


def _get_db_type(name: str) -> TypeDB:
    type_db = TypeDB.query.filter(TypeDB.name == name).first()
    if not type_db:
        raise ValidationError({'name': f'тип "{name}" не найден'})

    return type_db


def update_type(name: str, draft_type: Type) -> Tuple[Dict[str, str], int]:
    """
    Изменение нового пользовательского типа
    Если версия меньше последней то производится проверка на конфликты
    В случае перезаписи одинаковых данных возврщается ошибка marshmallow.ValidationError

    """
    _check_types_exists(draft_type.elements)

    saved_type = _get_db_type(name)
    if draft_type.version == saved_type.version:
        saved_type.elements = draft_type.dump_elements()
        saved_type.version += 1
        saved_type.updated = datetime.utcnow()

        db_session.commit()
        return TypeSchema().dump(saved_type.to_type()), 200

    diff = _compare_elements(saved_type.to_type(), draft_type)
    if diff.is_empty:
        return TypeSchema().dump(saved_type.to_type()), 200

    return DiffSchema().dump(diff), 400


def _compare_elements(saved_type: Type, draft_type: Type) -> Diff:
    saved_diff, draft_diff = saved_type.elements.copy(), draft_type.elements.copy()

    for el in saved_type.elements:
        if el in draft_type.elements:
            saved_diff.remove(el)
            draft_diff.remove(el)

    return Diff(saved=saved_diff, draft=draft_diff)
