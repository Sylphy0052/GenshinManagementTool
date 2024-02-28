from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from cruds.db import Base
from models.base import TimestampMixin


class Weapon(Base, TimestampMixin):  # type: ignore
    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, index=True)
    weapon_id = Column(Integer, ForeignKey("weapons_master.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    rare = Column(Integer, nullable=False)
    weapon_type = Column(String, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    t_level = Column(Integer, default=1, nullable=False)
    refine = Column(Integer, default=1, nullable=False)
    weapon = Column(String, nullable=False)
    enemy1 = Column(String, nullable=False)
    enemy2 = Column(String, nullable=False)
    is_get = Column(Boolean, default=False, nullable=False)
    is_calc = Column(Boolean, default=False, nullable=False)

    weapon_master = relationship("WeaponMaster", back_populates="player_weapon", uselist=False)

    def to_list(self) -> list[Column]:
        return [
            self.id,
            self.name,
            self.rare,
            self.weapon_type,
            self.level,
            self.t_level,
            self.refine,
            self.weapon,
            self.enemy1,
            self.enemy2,
            self.is_get,
            self.is_calc,
        ]

    def __repr__(self) -> str:
        return f"<Weapon: {self.name} Lv{self.level}>"
