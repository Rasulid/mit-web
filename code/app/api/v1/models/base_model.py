import re
import datetime
from sqlalchemy.orm import declared_attr, declarative_base
import sqlalchemy as db

from v1.exception import CustomValidationError
from core.babel_config import _


def camel_to_snake_case(text: str) -> str:
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', text).lower()


class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake_case(cls.__name__)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column("created_at", db.Date, default=datetime.datetime.utcnow)
    updated_at = db.Column("updated_at", db.Date, default=datetime.datetime.utcnow)
    deleted_at = db.Column(db.Date, default=None)


BaseModel = declarative_base(cls=BaseModel)


def base_validate_not_negative(key, value):
    if value < 0:
        raise CustomValidationError(_('Value should not be negative'))
    return value


def base_validate_positive(key, value):
    if value <= 0:
        raise CustomValidationError(_('Value should be positive'))
    return value


# https://stackoverflow.com/questions/27211361/sqlalchemy-declarative-inheritance-of-table-args
# https://stackoverflow.com/questions/63760639/sqlalchemy-checkconstraint-with-multiple-conditions-raises-warning
# https://stackoverflow.com/questions/20199462/sqlalchemy-postgresql-pg-regex
