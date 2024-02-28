import pandas as pd

from settings import CHARA_PATH, ITEM_PATH, WEAPON_PATH


def load_chara_csv() -> pd.DataFrame:
    chara_df = pd.read_csv(CHARA_PATH)
    return chara_df


def load_weapon_csv() -> pd.DataFrame:
    weapon_df = pd.read_csv(WEAPON_PATH)
    return weapon_df


def load_item_csv() -> pd.DataFrame:
    item_df = pd.read_csv(ITEM_PATH)
    return item_df
