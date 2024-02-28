from sqlalchemy import Boolean, Column, Integer, String

from cruds.db import Base
from models.base import TimestampMixin


class Chara(Base, TimestampMixin):  # type: ignore
    __tablename__ = "charas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    rare = Column(Integer, nullable=False)
    element = Column(String, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    t_level = Column(Integer, default=1, nullable=False)
    skill1 = Column(Integer, default=1, nullable=False)
    skill2 = Column(Integer, default=1, nullable=False)
    skill3 = Column(Integer, default=1, nullable=False)
    t_skill1 = Column(Integer, default=1, nullable=False)
    t_skill2 = Column(Integer, default=1, nullable=False)
    t_skill3 = Column(Integer, default=1, nullable=False)
    specialty = Column(String, nullable=False)
    enemy = Column(String, nullable=False)
    boss = Column(String, nullable=False)
    book = Column(String, nullable=False)
    weekly_boss = Column(String, nullable=False)
    is_get = Column(Boolean, default=False, nullable=False)
    is_calc = Column(Boolean, default=False, nullable=False)

    def to_list(self) -> list[Column]:
        return [
            self.id,
            self.name,
            self.rare,
            self.element,
            self.level,
            self.t_level,
            self.skill1,
            self.skill2,
            self.skill3,
            self.t_skill1,
            self.t_skill2,
            self.t_skill3,
            self.specialty,
            self.enemy,
            self.boss,
            self.book,
            self.weekly_boss,
            self.is_get,
            self.is_calc,
        ]

    def __repr__(self) -> str:
        return f"<Chara: {self.name} Lv{self.level} Skill: {self.skill1}-{self.skill2}-{self.skill3}>"
