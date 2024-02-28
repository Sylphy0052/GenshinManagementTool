import os
import shutil

import pandas as pd

from cruds.chara import update_chara_from_df
from cruds.item import update_item_from_df
from cruds.weapon import update_weapon_from_df
from func.chara import get_chara_df
from func.item import get_item_df
from func.weapon import get_player_weapon_df
from settings import FILE_DIR


def download_chara_csv() -> str:
    df = get_chara_df()
    df.to_csv(os.path.join(FILE_DIR, "chara.csv"), index=False)
    return os.path.join(FILE_DIR, "chara.csv")


def download_weapon_csv() -> str:
    df = get_player_weapon_df()
    df.to_csv(os.path.join(FILE_DIR, "weapon.csv"), index=False)
    return os.path.join(FILE_DIR, "weapon.csv")


def download_item_csv() -> str:
    df = get_item_df()
    df.to_csv(os.path.join(FILE_DIR, "item.csv"), index=False)
    return os.path.join(FILE_DIR, "item.csv")


def upload_chara_csv(file: str) -> None:
    shutil.copyfile(file.name, os.path.join(FILE_DIR, "up_chara.csv"))  # type: ignore
    chara_df = pd.read_csv(os.path.join(FILE_DIR, "up_chara.csv"))
    update_chara_from_df(chara_df)


def upload_weapon_csv(file: str) -> None:
    shutil.copyfile(file.name, os.path.join(FILE_DIR, "up_weapon.csv"))  # type: ignore
    weapon_df = pd.read_csv(os.path.join(FILE_DIR, "up_weapon.csv"))
    update_weapon_from_df(weapon_df)


def upload_item_csv(file: str) -> None:
    shutil.copyfile(file.name, os.path.join(FILE_DIR, "up_item.csv"))  # type: ignore
    item_df = pd.read_csv(os.path.join(FILE_DIR, "up_item.csv"))
    update_item_from_df(item_df)
