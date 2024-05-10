import logging

import numpy as np
from pandas import DataFrame

from cruds.item import read_item, update_num
from models.item import Item
from settings import ITEM_RENAME_COL, ITEM_RENAME_VALUES, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def get_item_df() -> DataFrame:
    item_list = read_item()
    columns = [item for item in Item.__table__.columns.keys() if item not in ["created_at", "updated_at"]]
    value_list = np.array([item.to_list() for item in item_list])
    if len(value_list) == 0:
        return DataFrame(columns=columns)
    item_df = DataFrame(value_list, columns=columns)
    return item_df


def _convert_show_values(item_df: DataFrame) -> DataFrame:
    item_df = item_df.rename(columns=ITEM_RENAME_COL)
    item_df = item_df.replace(ITEM_RENAME_VALUES)
    return item_df


def _filter_df(df: DataFrame, col: str, filter: str) -> DataFrame:
    if filter == "":
        return df
    else:
        return df[df[col] == filter]


def load_item_list_df(filter: str = "") -> DataFrame:
    item_df = get_item_df()
    item_df = _convert_show_values(item_df)
    item_df = _filter_df(item_df, "種類", filter)
    item_df = item_df.drop(columns=["base", "所持数"])
    return item_df


def load_player_item_df(filter: str = "") -> DataFrame:
    item_df = get_item_df()
    item_df = _convert_show_values(item_df)
    item_df = _filter_df(item_df, "種類", filter)
    item_df = item_df.drop(columns=["種類", "レア", "base"])
    item_df = item_df.reindex(columns=["id", "アイテム名", "所持数", "敵", "曜日"])
    return item_df


def change_player_item_df(new_item_df: DataFrame) -> DataFrame:
    new_item_df = new_item_df.drop(columns=["アイテム名", "敵", "曜日"])
    new_item_df = new_item_df.rename(columns={"所持数": "num"})
    item_df = get_item_df()
    item_df = _convert_show_values(item_df)
    item_df = item_df.drop(columns=["アイテム名", "種類", "レア", "base", "敵", "曜日"])
    item_df = item_df.rename(columns={"所持数": "num"})
    diff_df = item_df.merge(new_item_df, on="id", how="inner", suffixes=("_old", "_new"))
    diff_df = diff_df[diff_df["num_old"] != diff_df["num_new"]]
    diff_df = diff_df.drop(columns=["num_old"]).rename(columns={"num_new": "num"})
    update_num(diff_df.values.tolist())
    return load_player_item_df()
