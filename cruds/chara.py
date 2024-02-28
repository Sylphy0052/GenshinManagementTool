import logging

from pandas import DataFrame

from cruds.db import session as session_
from models.chara import Chara
from settings import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def create_chara_data(chara_datas: DataFrame) -> None:
    chara_list: list[Chara] = list()
    for _, chara_data in chara_datas.iterrows():
        chara = Chara(
            name=chara_data["name"],
            rare=chara_data["rare"],
            element=chara_data["element"],
            specialty=chara_data["specialty"],
            enemy=chara_data["enemy"],
            boss=chara_data["boss"],
            book=chara_data["book"],
            weekly_boss=chara_data["weekly_boss"],
        )
        chara_list.append(chara)
    with session_() as session:
        session.add_all(chara_list)
        session.commit()


def read_chara() -> list[Chara]:
    with session_() as session:
        chara_list = session.query(Chara).all()
    return chara_list  # type: ignore


def update_player_chara(diff_list: list[list[str]]) -> None:
    with session_() as session:
        for idx, is_get, level, t_level, skill1, t_skill1, skill2, t_skill2, skill3, t_skill3 in diff_list:
            chara = session.query(Chara).filter(Chara.id == idx).first()
            try:
                if 1 <= int(level) <= 90:
                    chara.level = int(level)  # type: ignore
                if 1 <= int(t_level) <= 90:
                    chara.t_level = int(t_level)  # type: ignore
                if 1 <= int(skill1) <= 10:
                    chara.skill1 = int(skill1)  # type: ignore
                if 1 <= int(skill2) <= 10:
                    chara.skill2 = int(skill2)  # type: ignore
                if 1 <= int(skill3) <= 10:
                    chara.skill3 = int(skill3)  # type: ignore
                if 1 <= int(t_skill1) <= 10:
                    chara.t_skill1 = int(t_skill1)  # type: ignore
                if 1 <= int(t_skill2) <= 10:
                    chara.t_skill2 = int(t_skill2)  # type: ignore
                if 1 <= int(t_skill3) <= 10:
                    chara.t_skill3 = int(t_skill3)  # type: ignore
                if is_get == "x" or is_get == "":
                    chara.is_get = is_get == "x"  # type: ignore
            except Exception as e:
                logger.error(e)
                continue
        session.commit()


def update_calc_target_chara(diff_list: list[list[str]]) -> None:
    with session_() as session:
        for idx, is_calc in diff_list:
            chara = session.query(Chara).filter(Chara.id == idx).first()
            try:
                if is_calc == "x" or is_calc == "":
                    chara.is_calc = is_calc == "x"  # type: ignore
            except Exception as e:
                logger.error(e)
                continue
        session.commit()


def update_chara_from_df(df: DataFrame) -> None:
    with session_() as session:
        for _, row in df.iterrows():
            chara = session.query(Chara).filter(Chara.name == row["name"]).first()
            try:
                if 1 <= int(row["level"]) <= 90:
                    chara.level = int(row["level"])  # type: ignore
                if 1 <= int(row["t_level"]) <= 90:
                    chara.t_level = int(row["t_level"])  # type: ignore
                if 1 <= int(row["skill1"]) <= 10:
                    chara.skill1 = int(row["skill1"])  # type: ignore
                if 1 <= int(row["skill2"]) <= 10:
                    chara.skill2 = int(row["skill2"])  # type: ignore
                if 1 <= int(row["skill3"]) <= 10:
                    chara.skill3 = int(row["skill3"])  # type: ignore
                if 1 <= int(row["t_skill1"]) <= 10:
                    chara.t_skill1 = int(row["t_skill1"])  # type: ignore
                if 1 <= int(row["t_skill2"]) <= 10:
                    chara.t_skill2 = int(row["t_skill2"])  # type: ignore
                if 1 <= int(row["t_skill3"]) <= 10:
                    chara.t_skill3 = int(row["t_skill3"])  # type: ignore
                if isinstance(row["is_get"], bool):
                    chara.is_get = row["is_get"]  # type: ignore
                if isinstance(row["is_calc"], bool):
                    chara.is_calc = row["is_calc"]  # type: ignore
            except Exception as e:
                logger.error(e)
                continue
        session.commit()


def update_chara_lv(diff_list: list[list[int]]) -> None:
    with session_() as session:
        for idx, level in diff_list:
            chara = session.query(Chara).filter(Chara.id == idx).first()
            try:
                chara.level = int(level)  # type: ignore
            except Exception as e:
                logger.error(e)
                continue
        session.commit()


def update_chara_skill1(diff_list: list[list[int]]) -> None:
    with session_() as session:
        for idx, skill1 in diff_list:
            chara = session.query(Chara).filter(Chara.id == idx).first()
            try:
                chara.skill1 = int(skill1)  # type: ignore
            except Exception as e:
                logger.error(e)
                continue
        session.commit()


def update_chara_skill2(diff_list: list[list[int]]) -> None:
    with session_() as session:
        for idx, skill2 in diff_list:
            chara = session.query(Chara).filter(Chara.id == idx).first()
            try:
                chara.skill2 = int(skill2)  # type: ignore
            except Exception as e:
                logger.error(e)
                continue
        session.commit()


def update_chara_skill3(diff_list: list[list[int]]) -> None:
    with session_() as session:
        for idx, skill3 in diff_list:
            chara = session.query(Chara).filter(Chara.id == idx).first()
            try:
                chara.skill3 = int(skill3)  # type: ignore
            except Exception as e:
                logger.error(e)
                continue
        session.commit()
