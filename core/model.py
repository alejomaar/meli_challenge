from sqlalchemy import (
    BigInteger,
    Column,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Base(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True,
        nullable=False,
        comment="unique identifier for the entity",
    )

    def as_dict(self):
        """
        Convert the SQLAlchemy model to a dictionary, including only columns whose
        type is one of the allowed types: strings, numbers, and booleans.
        """
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if isinstance(c.type, self.__allowed_types__)
        }
