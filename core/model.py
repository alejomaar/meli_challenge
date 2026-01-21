from sqlalchemy import BigInteger, Column
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
