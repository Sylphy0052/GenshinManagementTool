import logging

from pandas import DataFrame

from cruds.db import session as session_
from models.weapon import Weapon
from models.weapon_master import WeaponMaster
from settings import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def create_weapon_data(weapon_datas: DataFrame) -> None:
    weapon_list: list[Weapon] = list()
    for _, weapon_data in weapon_datas.iterrows():
        weapon = WeaponMaster(
            name=weapon_data["name"],
            rare=weapon_data["rare"],
            weapon_type=weapon_data["weapon_type"],
            weapon=weapon_data["weapon"],
            enemy1=weapon_data["enemy1"],
            enemy2=weapon_data["enemy2"],
        )
        weapon_list.append(weapon)
    with session_() as session:
        session.add_all(weapon_list)
        session.commit()


def read_weapon() -> list[WeaponMaster]:
    with session_() as session:
        weapon_list = session.query(WeaponMaster).all()
    return weapon_list  # type: ignore


def read_player_weapon() -> list[Weapon]:
    with session_() as session:
        weapon_list = session.query(Weapon).all()
    return weapon_list  # type: ignore


def update_player_weapon(diff_list: list[list[str]]) -> None:
    with session_() as session:
        for idx, is_get, level, t_level, refine in diff_list:
            weapon = session.query(Weapon).filter(Weapon.id == idx).first()
            level = int(level) if 1 <= int(level) <= 90 else 1  # type: ignore
            t_level = int(t_level) if 1 <= int(t_level) <= 90 else 1  # type: ignore
            refine = int(refine) if 1 <= int(refine) <= 5 else 1  # type: ignore
            try:
                weapon.level = level  # type: ignore
                weapon.t_level = t_level  # type: ignore
                weapon.refine = refine  # type: ignore
                weapon.is_get = is_get == "x"  # type: ignore
            except Exception as e:
                logger.error(e)
                session.rollback()
                return
        session.commit()


def update_weapon_from_df(df: DataFrame) -> None:
    with session_() as session:
        weapon_list = list()
        for _, row in df.iterrows():
            weapon_master = session.query(WeaponMaster).filter(WeaponMaster.name == row["name"]).first()
            level = int(row["level"]) if 1 <= int(row["level"]) <= 90 else 1
            t_level = int(row["t_level"]) if 1 <= int(row["t_level"]) <= 90 else 1
            refine = int(row["refine"]) if 1 <= int(row["refine"]) <= 5 else 1
            is_get = bool(row["is_get"])
            is_calc = bool(row["is_calc"])
            try:
                weapon = Weapon(
                    name=weapon_master.name,  # type: ignore
                    rare=weapon_master.rare,  # type: ignore
                    weapon_type=weapon_master.weapon_type,  # type: ignore
                    level=level,
                    t_level=t_level,
                    refine=refine,
                    weapon=weapon_master.weapon,  # type: ignore
                    enemy1=weapon_master.enemy1,  # type: ignore
                    enemy2=weapon_master.enemy2,  # type: ignore
                    is_get=is_get,
                    is_calc=is_calc,
                    weapon_master=weapon_master,
                )
                weapon_list.append(weapon)
            except Exception as e:
                logger.error(e)
                logger.error(row)
                session.rollback()
                return
        session.add_all(weapon_list)
        session.commit()


def add_player_weapon(name: str, level: int, refine: int, is_get: bool, is_calc: bool) -> None:
    with session_() as session:
        weapon_master = session.query(WeaponMaster).filter(WeaponMaster.name == name).first()
        level = level if 1 <= level <= 90 else 1
        refine = refine if 1 <= refine <= 5 else 1
        try:
            weapon = Weapon(
                name=weapon_master.name,  # type: ignore
                rare=weapon_master.rare,  # type: ignore
                weapon_type=weapon_master.weapon_type,  # type: ignore
                level=level,
                t_level=1,
                refine=refine,
                weapon=weapon_master.weapon,  # type: ignore
                enemy1=weapon_master.enemy1,  # type: ignore
                enemy2=weapon_master.enemy2,  # type: ignore
                is_get=is_get,
                is_calc=is_calc,
                weapon_master=weapon_master,
            )
            session.add(weapon)
        except Exception as e:
            logger.error(e)
            session.rollback()
            return
        session.commit()


def delete_player_weapon(weapon_id: int) -> None:
    with session_() as session:
        weapon = session.query(Weapon).filter(Weapon.id == weapon_id).first()
        try:
            session.delete(weapon)
        except Exception as e:
            logger.error(e)
            session.rollback()
            return
        session.commit()


def update_calc_weapon(diff_list: list[list[str]]) -> None:
    with session_() as session:
        for idx, is_calc in diff_list:
            weapon = session.query(Weapon).filter(Weapon.id == idx).first()
            try:
                weapon.is_calc = is_calc == "x"  # type: ignore
            except Exception as e:
                logger.error(e)
                session.rollback()
                return
        session.commit()


def update_weapon_lv(diff_list: list[list[str | int]]) -> None:
    with session_() as session:
        for idx, lv in diff_list:
            weapon = session.query(Weapon).filter(Weapon.id == idx).first()
            try:
                weapon.level = int(lv)  # type: ignore
            except Exception as e:
                logger.error(e)
                session.rollback()
                return
        session.commit()
