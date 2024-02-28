from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped


class TimestampMixin:
    @declared_attr  # type: ignore
    def created_at(cls) -> Mapped[datetime]:
        return Column(DateTime, default=datetime.now(), nullable=False)  # type: ignore

    @declared_attr  # type: ignore
    def updated_at(cls) -> Mapped[datetime]:
        return Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)  # type: ignore
