import logging
import os

import pandas as pd

from cruds.chara import create_chara_data, update_chara_from_df
from cruds.db import Base, engine
from cruds.item import create_item_data, update_item_from_df
from cruds.weapon import create_weapon_data, update_weapon_from_df
from data_loader.read_csv import load_chara_csv, load_item_csv, load_weapon_csv
from func.file import download_chara_csv, download_item_csv, download_weapon_csv
from settings import FILE_DIR, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def _init_db() -> None:
    chara_data = load_chara_csv()
    create_chara_data(chara_data)
    weapon_data = load_weapon_csv()
    create_weapon_data(weapon_data)
    item_data = load_item_csv()
    create_item_data(item_data)


def create_db() -> None:
    Base.metadata.create_all(engine)


def reset_db() -> None:
    logger.info("Resetting DB")
    download_chara_csv()
    download_weapon_csv()
    download_item_csv()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    _init_db()
    # キャラ情報復元
    chara_path = os.path.join(FILE_DIR, "chara.csv")
    if os.path.exists(chara_path):
        chara_df = pd.read_csv(chara_path)
        update_chara_from_df(chara_df)
    # 武器情報復元
    weapon_path = os.path.join(FILE_DIR, "weapon.csv")
    if os.path.exists(weapon_path):
        weapon_df = pd.read_csv(weapon_path)
        update_weapon_from_df(weapon_df)
    # 素材情報復元
    item_path = os.path.join(FILE_DIR, "item.csv")
    if os.path.exists(item_path):
        item_df = pd.read_csv(item_path)
        update_item_from_df(item_df)


if __name__ == "__main__":
    reset_db()
