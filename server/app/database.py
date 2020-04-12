from uuid import UUID, uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as postgres_UUID
from sqlalchemy.types import CHAR, TypeDecorator

db = SQLAlchemy()


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(postgres_UUID())

        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if not value:
            return value
        elif dialect.name == "postgresql":
            return str(value)

        if not isinstance(value, UUID):
            return "%.32x" % int(UUID(value))

        return "%.32x" % value.int  # hexstring

    def process_result_value(self, value, dialect):
        if not value:
            return value

        return UUID(value)


class CRUDMixin(object):
    id = db.Column(GUID, primary_key=True, nullable=False, default=lambda: str(uuid4()))

    @classmethod
    def get_or_create(cls, **kwargs):
        instance = cls.query.find_by(**kwargs).first()
        if instance:
            instance.update(**kwargs)
            return instance
        return cls.create(kwargs)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def flush(self):
        db.session.flush()
        return self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()
