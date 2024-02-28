from sqlalchemy import Column, Integer, String

from cruds.db import Base
from models.base import TimestampMixin


class Item(Base, TimestampMixin):  # type: ignore
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    item_type = Column(String, nullable=False)
    rare = Column(Integer)
    base = Column(String)
    enemy = Column(String)
    week = Column(String)
    num = Column(Integer, default=0, nullable=False)

    def to_list(self) -> list[Column]:
        return [
            self.id,
            self.name,
            self.item_type,
            self.rare,
            self.base,
            self.enemy,
            self.week,
            self.num,
        ]

    def __repr__(self) -> str:
        return f"<Item: {self.name} Type: {self.item_type} Rare: {self.rare}>"
