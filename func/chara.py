import logging

import numpy as np
from pandas import DataFrame

from cruds.chara import read_chara, update_calc_target_chara, update_player_chara
from models.chara import Chara
from settings import CHARA_RENAME_COL, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def get_chara_df() -> DataFrame:
    chara_list = read_chara()
    columns = [chara for chara in Chara.__table__.columns.keys() if chara not in ["created_at", "updated_at"]]
    value_list = np.array([chara.to_list() for chara in chara_list])
    if len(value_list) == 0:
        return DataFrame(columns=columns)
    chara_df = DataFrame(value_list, columns=columns)
    return chara_df


def _convert_show_values(chara_df: DataFrame) -> DataFrame:
    chara_df = chara_df.replace({"is_get": {"True": "x", "False": ""}})
    chara_df = chara_df.replace({"is_calc": {"True": "x", "False": ""}})
    chara_df = chara_df.rename(columns=CHARA_RENAME_COL)
    return chara_df


def _filter_df(
    df: DataFrame, rare_filter: str, element_filter: str, get_filter: bool = False, calc_filter: bool = False
) -> DataFrame:
    if rare_filter != "":
        df = df[df["レア"] == rare_filter]
    if element_filter != "":
        df = df[df["属性"] == element_filter]
    if get_filter:
        df = df[df["入手"] == "x"]
    if calc_filter:
        df = df[df["計算対象"] == "x"]
    return df


def load_chara_list_df(
    rare_filter: str = "", element_filter: str = "", get_filter: bool = False, calc_filter: bool = False
) -> DataFrame:
    chara_df = get_chara_df()
    chara_df = _convert_show_values(chara_df)
    chara_df = _filter_df(chara_df, rare_filter, element_filter, get_filter, calc_filter)
    chara_df = chara_df.drop(
        columns=[
            "Lv",
            "目標Lv",
            "通常攻撃",
            "スキル",
            "元素爆発",
            "目標:通常攻撃",
            "目標:スキル",
            "目標:元素爆発",
            "入手",
            "計算対象",
        ]
    )
    return chara_df


def load_player_chara_df(
    rare_filter: str = "", element_filter: str = "", get_filter: bool = False, calc_filter: bool = False
) -> DataFrame:
    chara_df = get_chara_df()
    chara_df = _convert_show_values(chara_df)
    chara_df = _filter_df(chara_df, rare_filter, element_filter, get_filter, calc_filter)
    chara_df = chara_df.drop(columns=["特産品", "敵", "ボス", "本", "週ボス", "計算対象"])
    chara_df = chara_df.reindex(
        columns=[
            "id",
            "入手",
            "キャラ名",
            "レア",
            "属性",
            "Lv",
            "目標Lv",
            "通常攻撃",
            "目標:通常攻撃",
            "スキル",
            "目標:スキル",
            "元素爆発",
            "目標:元素爆発",
        ]
    )
    return chara_df


def load_calc_target_chara_df(
    rare_filter: str = "", element_filter: str = "", get_filter: bool = False, calc_filter: bool = False
) -> DataFrame:
    chara_df = get_chara_df()
    chara_df = _convert_show_values(chara_df)
    chara_df = _filter_df(chara_df, rare_filter, element_filter, get_filter, calc_filter)
    chara_df["Lv"] = chara_df["Lv"] + " -> " + chara_df["目標Lv"]
    chara_df["通常攻撃"] = chara_df["通常攻撃"] + " -> " + chara_df["目標:通常攻撃"]
    chara_df["スキル"] = chara_df["スキル"] + " -> " + chara_df["目標:スキル"]
    chara_df["元素爆発"] = chara_df["元素爆発"] + " -> " + chara_df["目標:元素爆発"]
    chara_df = chara_df.drop(
        columns=[
            "目標Lv",
            "目標:通常攻撃",
            "目標:スキル",
            "目標:元素爆発",
            "特産品",
            "敵",
            "ボス",
            "本",
            "週ボス",
            "入手",
        ]
    )
    chara_df = chara_df.reindex(
        columns=[
            "id",
            "計算対象",
            "キャラ名",
            "レア",
            "属性",
            "Lv",
            "通常攻撃",
            "スキル",
            "元素爆発",
        ]
    )
    return chara_df


def _get_player_chara_diff(old_df: DataFrame, new_df: DataFrame) -> DataFrame:
    remove_cols = ["キャラ名", "レア", "属性"]
    old_df = old_df.drop(columns=remove_cols)
    new_df = new_df.drop(columns=remove_cols)
    diff_df = old_df.merge(new_df, on="id", how="inner", suffixes=("_old", "_new"))
    diff_df = diff_df[
        (diff_df["Lv_old"] != diff_df["Lv_new"])
        | (diff_df["目標Lv_old"] != diff_df["目標Lv_new"])
        | (diff_df["通常攻撃_old"] != diff_df["通常攻撃_new"])
        | (diff_df["スキル_old"] != diff_df["スキル_new"])
        | (diff_df["元素爆発_old"] != diff_df["元素爆発_new"])
        | (diff_df["目標:通常攻撃_old"] != diff_df["目標:通常攻撃_new"])
        | (diff_df["目標:スキル_old"] != diff_df["目標:スキル_new"])
        | (diff_df["目標:元素爆発_old"] != diff_df["目標:元素爆発_new"])
        | (diff_df["入手_old"] != diff_df["入手_new"])
    ]
    diff_df = diff_df.drop(
        columns=[
            "Lv_old",
            "目標Lv_old",
            "通常攻撃_old",
            "スキル_old",
            "元素爆発_old",
            "目標:通常攻撃_old",
            "目標:スキル_old",
            "目標:元素爆発_old",
            "入手_old",
        ]
    ).rename(
        columns={
            "Lv_new": "level",
            "目標Lv_new": "t_level",
            "通常攻撃_new": "skill1",
            "スキル_new": "skill2",
            "元素爆発_new": "skill3",
            "目標:通常攻撃_new": "t_skill1",
            "目標:スキル_new": "t_skill2",
            "目標:元素爆発_new": "t_skill3",
            "入手_new": "is_get",
        }
    )
    return diff_df


def change_player_chara_df(
    new_chara_df: DataFrame,
    rare_filter: str = "",
    element_filter: str = "",
    get_filter: bool = False,
    calc_filter: bool = False,
) -> DataFrame:
    new_chara_df.loc[new_chara_df["入手"] == "x", "入手"] = "x"
    new_chara_df.loc[new_chara_df["入手"] != "x", "入手"] = ""
    chara_df = get_chara_df()
    chara_df = _convert_show_values(chara_df)
    chara_df = chara_df.drop(columns=["特産品", "敵", "ボス", "本", "週ボス", "計算対象"])
    diff_df = _get_player_chara_diff(chara_df, new_chara_df)
    update_player_chara(diff_df.values.tolist())
    return load_player_chara_df(rare_filter, element_filter, get_filter, calc_filter)


def _get_calc_target_chara_diff(old_df: DataFrame, new_df: DataFrame) -> DataFrame:
    remove_cols = [
        "キャラ名",
        "レア",
        "属性",
        "Lv",
        "通常攻撃",
        "スキル",
        "元素爆発",
    ]
    old_df = old_df.drop(columns=remove_cols)
    new_df = new_df.drop(columns=remove_cols)
    diff_df = old_df.merge(new_df, on="id", how="inner", suffixes=("_old", "_new"))
    diff_df = diff_df[(diff_df["計算対象_old"] != diff_df["計算対象_new"])]
    diff_df = diff_df.drop(columns=["計算対象_old"]).rename(columns={"計算対象_new": "is_calc"})
    return diff_df


def change_calc_target_chara_df(
    new_chara_df: DataFrame,
    rare_filter: str = "",
    element_filter: str = "",
    get_filter: bool = False,
    calc_filter: bool = False,
) -> DataFrame:
    new_chara_df.loc[new_chara_df["計算対象"] == "x", "計算対象"] = "x"
    new_chara_df.loc[new_chara_df["計算対象"] != "x", "計算対象"] = ""
    chara_df = get_chara_df()
    chara_df = _convert_show_values(chara_df)
    chara_df = _filter_df(chara_df, rare_filter, element_filter, get_filter, calc_filter)
    chara_df = chara_df.drop(
        columns=[
            "目標Lv",
            "目標:通常攻撃",
            "目標:スキル",
            "目標:元素爆発",
            "特産品",
            "敵",
            "ボス",
            "本",
            "週ボス",
            "入手",
        ]
    )
    diff_df = _get_calc_target_chara_diff(chara_df, new_chara_df)
    update_calc_target_chara(diff_df.values.tolist())
    return load_calc_target_chara_df(rare_filter, element_filter, get_filter, calc_filter)
