from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from cruds.db import Base
from models.base import TimestampMixin


class WeaponMaster(Base, TimestampMixin):  # type: ignore
    __tablename__ = "weapons_master"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    rare = Column(Integer, nullable=False)
    weapon_type = Column(String, nullable=False)
    weapon = Column(String, nullable=False)
    enemy1 = Column(String, nullable=False)
    enemy2 = Column(String, nullable=False)

    player_weapon = relationship("Weapon", back_populates="weapon_master")

    def to_list(self) -> list[Column]:
        return [
            self.id,
            self.name,
            self.rare,
            self.weapon_type,
            self.weapon,
            self.enemy1,
            self.enemy2,
        ]

    def __repr__(self) -> str:
        return f"<Weapon: {self.name} {self.rare} {self.weapon_type}>"
