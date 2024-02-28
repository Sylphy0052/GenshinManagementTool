import logging

import numpy as np
from pandas import DataFrame

from cruds.weapon import (
    add_player_weapon,
    delete_player_weapon,
    read_player_weapon,
    read_weapon,
    update_calc_weapon,
    update_player_weapon,
)
from models.weapon import Weapon
from models.weapon_master import WeaponMaster
from settings import LOGGER_NAME, MASTER_WEAPON_RENAME_COL, WEAPON_RENAME_COL

logger = logging.getLogger(LOGGER_NAME)


def get_weapon_df() -> DataFrame:
    weapon_list = read_weapon()
    columns = [
        weapon for weapon in WeaponMaster.__table__.columns.keys() if weapon not in ["created_at", "updated_at"]
    ]
    value_list = np.array([weapon.to_list() for weapon in weapon_list])
    weapon_df = DataFrame(value_list, columns=columns)
    return weapon_df


def get_player_weapon_df() -> DataFrame:
    weapon_list = read_player_weapon()
    columns = [
        weapon for weapon in Weapon.__table__.columns.keys() if weapon not in ["weapon_id", "created_at", "updated_at"]
    ]
    value_list = np.array([weapon.to_list() for weapon in weapon_list])
    if len(value_list) == 0:
        return DataFrame(columns=columns)
    weapon_df = DataFrame(value_list, columns=columns)
    return weapon_df


def _convert_master_show_values(weapon_df: DataFrame) -> DataFrame:
    weapon_df = weapon_df.rename(columns=MASTER_WEAPON_RENAME_COL)
    return weapon_df


def _convert_show_values(weapon_df: DataFrame) -> DataFrame:
    weapon_df = weapon_df.replace({"is_get": {"True": "x", "False": ""}})
    weapon_df = weapon_df.replace({"is_calc": {"True": "x", "False": ""}})
    weapon_df = weapon_df.rename(columns=WEAPON_RENAME_COL)
    return weapon_df


def _filter_df(
    df: DataFrame, rare_filter: str, type_filter: str, get_filter: bool = False, calc_filter: bool = False
) -> DataFrame:
    if rare_filter != "":
        df = df[df["レア"] == rare_filter]
    if type_filter != "":
        df = df[df["武器種"] == type_filter]
    if get_filter:
        df = df[df["入手"] == "x"]
    if calc_filter:
        df = df[df["計算対象"] == "x"]
    return df


def load_weapon_list_df(rare_filter: str = "", type_filter: str = "") -> DataFrame:
    weapon_df = get_weapon_df()
    weapon_df = _convert_master_show_values(weapon_df)
    weapon_df = _filter_df(weapon_df, rare_filter, type_filter)
    return weapon_df


def load_player_weapon_df(
    rare_filter: str = "", type_filter: str = "", get_filter: bool = False, calc_filter: bool = False
) -> DataFrame:
    weapon_df = get_player_weapon_df()
    weapon_df = _convert_show_values(weapon_df)
    weapon_df = _filter_df(weapon_df, rare_filter, type_filter, get_filter, calc_filter)
    weapon_df = weapon_df.drop(columns=["武器素材", "敵1", "敵2", "計算対象"])
    weapon_df = weapon_df.reindex(columns=["id", "入手", "武器名", "レア", "武器種", "Lv", "目標Lv", "精錬"])
    return weapon_df


def _get_player_weapon_diff(old_df: DataFrame, new_df: DataFrame) -> DataFrame:
    remove_cols = ["武器名", "レア", "武器種"]
    old_df = old_df.drop(columns=remove_cols)
    new_df = new_df.drop(columns=remove_cols)
    diff_df = old_df.merge(new_df, on="id", how="inner", suffixes=("_old", "_new"))
    diff_df = diff_df[
        (diff_df["Lv_old"] != diff_df["Lv_new"])
        | (diff_df["目標Lv_old"] != diff_df["目標Lv_new"])
        | (diff_df["精錬_old"] != diff_df["精錬_new"])
        | (diff_df["入手_old"] != diff_df["入手_new"])
    ]
    diff_df = diff_df.drop(columns=["Lv_old", "目標Lv_old", "精錬_old", "入手_old"]).rename(
        columns={"Lv_new": "level", "目標Lv_new": "t_level", "精錬_new": "refine", "入手_new": "is_get"}
    )
    return diff_df


def change_player_weapon_df(
    new_weapon_df: DataFrame,
    rare_filter: str = "",
    type_filter: str = "",
    get_filter: bool = False,
    calc_filter: bool = False,
) -> DataFrame:
    new_weapon_df.loc[new_weapon_df["入手"] == "x", "入手"] = "x"
    new_weapon_df.loc[new_weapon_df["入手"] != "x", "入手"] = ""
    weapon_df = get_player_weapon_df()
    weapon_df = _convert_show_values(weapon_df)
    weapon_df = weapon_df.drop(columns=["武器素材", "敵1", "敵2", "計算対象"])
    diff_df = _get_player_weapon_diff(weapon_df, new_weapon_df)
    update_player_weapon(diff_df.values.tolist())
    return load_player_weapon_df(rare_filter, type_filter, get_filter, calc_filter)


def get_weapon_list(rare_filter: str = "", type_filter: str = "") -> list[str]:
    weapon_df = load_weapon_list_df(rare_filter, type_filter)
    weapon_list = [""]
    weapon_list.extend(weapon_df["武器名"].tolist())
    return weapon_list


def get_weapon_detail_list(rare_filter: str = "", type_filter: str = "") -> list[str]:
    weapon_df = load_player_weapon_df(rare_filter, type_filter)
    weapon_list = [""]
    weapon_list.extend(
        [f"{x['id']}: {x['武器名']} Lv{x['Lv']}->{x['目標Lv']} 精錬{x['精錬']}" for _, x in weapon_df.iterrows()]
    )
    return weapon_list


def get_get_weapon_detail_list(rare_filter: str = "", type_filter: str = "") -> list[str]:
    weapon_df = load_player_weapon_df(rare_filter, type_filter, True)
    weapon_list = [""]
    weapon_list.extend(
        [f"{x['id']}: {x['武器名']} Lv{x['Lv']}->{x['目標Lv']} 精錬{x['精錬']}" for _, x in weapon_df.iterrows()]
    )
    return weapon_list


def add_weapon(name: str, lv: int, refine: int, is_get: bool, is_calc: bool) -> None:
    if name != "":
        add_player_weapon(name, lv, refine, is_get, is_calc)


def delete_weapon(weapon_info: str) -> None:
    if weapon_info != "":
        weapon_id = int(weapon_info.split(":")[0])
        delete_player_weapon(weapon_id)


def load_calc_weapon_df(
    rare_filter: str = "",
    type_filter: str = "",
    get_filter: bool = False,
    calc_filter: bool = False,
) -> DataFrame:
    weapon_df = get_player_weapon_df()
    weapon_df = _convert_show_values(weapon_df)
    weapon_df = _filter_df(weapon_df, rare_filter, type_filter, get_filter, calc_filter)
    weapon_df["Lv"] = weapon_df["Lv"] + " -> " + weapon_df["目標Lv"]
    weapon_df = weapon_df.drop(columns=["目標Lv", "武器素材", "敵1", "敵2", "入手"])
    weapon_df = weapon_df.reindex(columns=["id", "計算対象", "武器名", "レア", "武器種", "Lv", "精錬"])
    return weapon_df


def _get_calc_weapon_diff(old_df: DataFrame, new_df: DataFrame) -> DataFrame:
    remove_cols = ["武器名", "レア", "武器種", "Lv", "精錬"]
    old_df = old_df.drop(columns=remove_cols)
    new_df = new_df.drop(columns=remove_cols)
    diff_df = old_df.merge(new_df, on="id", how="inner", suffixes=("_old", "_new"))
    diff_df = diff_df[diff_df["計算対象_old"] != diff_df["計算対象_new"]]
    diff_df = diff_df.drop(columns=["計算対象_old"]).rename(columns={"計算対象_new": "is_calc"})
    return diff_df


def change_calc_weapon_df(
    new_weapon_df: DataFrame,
    rare_filter: str = "",
    type_filter: str = "",
    get_filter: bool = False,
    calc_filter: bool = False,
) -> DataFrame:
    new_weapon_df.loc[new_weapon_df["計算対象"] == "x", "計算対象"] = "x"
    new_weapon_df.loc[new_weapon_df["計算対象"] != "x", "計算対象"] = ""
    weapon_df = get_player_weapon_df()
    weapon_df = _convert_show_values(weapon_df)
    weapon_df = _filter_df(weapon_df, rare_filter, type_filter, get_filter, calc_filter)
    weapon_df["Lv"] = weapon_df["Lv"] + " -> " + weapon_df["目標Lv"]
    weapon_df = weapon_df.drop(columns=["目標Lv", "武器素材", "敵1", "敵2", "入手"])
    weapon_df = weapon_df.reindex(columns=["id", "計算対象", "武器名", "レア", "武器種", "Lv", "精錬"])
    diff_df = _get_calc_weapon_diff(weapon_df, new_weapon_df)
    update_calc_weapon(diff_df.values.tolist())
    return load_calc_weapon_df(rare_filter, type_filter, get_filter, calc_filter)
