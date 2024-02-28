from pandas import DataFrame

from cruds.item import update_num
from func.chara import get_chara_df
from func.item import get_item_df
from func.weapon import get_player_weapon_df
from settings import (
    ELEMENT_STONE,
    ITEM_RENAME_VALUES,
    NEED_LV_ITEM,
    NEED_SKILL_ITEM,
    WEAPON3_LV_ITEM,
    WEAPON4_LV_ITEM,
    WEAPON5_LV_ITEM,
)


def _calc_lv_item(chara_df: DataFrame, weapon_df: DataFrame, item_df: DataFrame) -> DataFrame:
    lv_values: dict[int, list[int | str]] = dict()
    for _, chara in chara_df.iterrows():
        # Level
        if int(chara["level"]) < int(chara["t_level"]):
            lv_list = [lv for lv in range(int(chara["level"]), int(chara["t_level"]) + 1) if lv in NEED_LV_ITEM]
            if len(lv_list) > 0:
                for lv in lv_list:
                    for item_type, (rare, num) in NEED_LV_ITEM[lv].items():
                        if item_type == "stone":
                            item = ELEMENT_STONE[chara["element"]]
                        else:
                            item = chara[item_type]
                        if item_df[item_df["base"] == item].shape[0] == 0:
                            print(chara)
                            print(item)
                        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
                        if item_s["id"] in lv_values:
                            lv_values[item_s["id"]][3] += num  # type: ignore
                        else:
                            lv_values[item_s["id"]] = [
                                item_s["id"],
                                item_s["name"],
                                item_s["num"],
                                num,
                                item_s["item_type"],
                                item_s["rare"],
                                item_s["enemy"],
                                item_s["week"],
                            ]
        # スキル
        for i in [1, 2, 3]:
            s, t = f"skill{i}", f"t_skill{i}"
            if int(chara[s]) < int(chara[t]):
                lv_list = [lv for lv in range(int(chara[s]) + 1, int(chara[t]) + 1) if lv in NEED_SKILL_ITEM]
                if len(lv_list) > 0:
                    for lv in lv_list:
                        for item_type, (rare, num) in NEED_SKILL_ITEM[lv].items():
                            if item_type == "special":
                                item_s = item_df[item_df["item_type"] == item_type].iloc[0]
                            else:
                                item = chara[item_type]
                                item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
                            if item_s["id"] in lv_values:
                                lv_values[item_s["id"]][3] += num  # type: ignore
                            else:
                                lv_values[item_s["id"]] = [
                                    item_s["id"],
                                    item_s["name"],
                                    item_s["num"],
                                    num,
                                    item_s["item_type"],
                                    item_s["rare"],
                                    item_s["enemy"],
                                    item_s["week"],
                                ]
    for _, weapon in weapon_df.iterrows():
        # Level
        if int(weapon["level"]) < int(weapon["t_level"]):
            weapon_lv_item = dict()
            if int(weapon["rare"]) == 5:
                weapon_lv_item = WEAPON5_LV_ITEM
            elif int(weapon["rare"]) == 4:
                weapon_lv_item = WEAPON4_LV_ITEM
            elif int(weapon["rare"]) == 3:
                weapon_lv_item = WEAPON3_LV_ITEM
            else:
                continue
            lv_list = [lv for lv in range(int(weapon["level"]), int(weapon["t_level"]) + 1) if lv in weapon_lv_item]
            if len(lv_list) > 0:
                for lv in lv_list:
                    for item_type, (rare, num) in weapon_lv_item[lv].items():
                        item = weapon[item_type]
                        if item_df[item_df["base"] == item].shape[0] == 0:
                            print(weapon)
                            print(item)
                        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
                        if item_s["id"] in lv_values:
                            lv_values[item_s["id"]][3] += num  # type: ignore
                        else:
                            lv_values[item_s["id"]] = [
                                item_s["id"],
                                item_s["name"],
                                item_s["num"],
                                num,
                                item_s["item_type"],
                                item_s["rare"],
                                item_s["enemy"],
                                item_s["week"],
                            ]
    lv_df = DataFrame.from_dict(
        lv_values, columns=["id", "アイテム名", "所持数", "必要数", "種類", "レア", "敵", "曜日"], orient="index"
    ).sort_index()
    return lv_df


def load_calc_item_df(need_filter: bool = False) -> DataFrame:
    chara_df = get_chara_df()
    weapon_df = get_player_weapon_df()
    item_df = get_item_df()

    chara_df = chara_df[chara_df["is_calc"] == "True"]
    weapon_df = weapon_df[weapon_df["is_calc"] == "True"]
    calc_item_df = _calc_lv_item(chara_df, weapon_df, item_df)
    calc_item_df["差分"] = calc_item_df["必要数"] - calc_item_df["所持数"]
    calc_item_df.loc[calc_item_df["差分"] < 0, "差分"] = 0
    calc_item_df = calc_item_df.replace(ITEM_RENAME_VALUES)
    calc_item_df = calc_item_df.reindex(
        columns=["id", "アイテム名", "所持数", "必要数", "差分", "種類", "レア", "敵", "曜日"]
    )
    if need_filter:
        calc_item_df = calc_item_df[calc_item_df["差分"] > 0]
    return calc_item_df


def change_calc_item_df(new_need_item_df: DataFrame, need_filter: bool = False) -> DataFrame:
    drop_columns = ["アイテム名", "必要数", "差分", "種類", "レア", "敵", "曜日"]
    rename_columns = {"所持数": "num"}
    new_need_item_df = new_need_item_df.drop(columns=drop_columns)
    new_need_item_df = new_need_item_df.rename(columns=rename_columns)
    need_item_df = load_calc_item_df()
    if need_filter:
        need_item_df = need_item_df[need_item_df["差分"] > 0]
    need_item_df = need_item_df.drop(columns=drop_columns)
    need_item_df = need_item_df.rename(columns=rename_columns)
    diff_df = need_item_df.merge(new_need_item_df, on="id", how="inner", suffixes=("_old", "_new"))
    diff_df = diff_df[diff_df["num_old"] != diff_df["num_new"]]
    diff_df = diff_df.drop(columns=["num_old"]).rename(columns={"num_new": "num"})
    update_num(diff_df.values.tolist())
    return load_calc_item_df(need_filter)


def _calc_total_item(item_df: DataFrame, need_item_df: DataFrame) -> DataFrame:
    columns = [
        "ベースアイテム",
        "所持数",
        "必要数",
        "差分",
        "所持レア1",
        "所持レア2",
        "所持レア3",
        "所持レア4",
        "必要レア1",
        "必要レア2",
        "必要レア3",
        "必要レア4",
        "曜日",
    ]
    need_item_df_ = need_item_df.merge(item_df, on="id", how="left")
    base_list = list(set([b for b in need_item_df_["base"]]))
    df_values = [[base, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ""] for base in base_list]
    total_item_df = DataFrame(df_values, columns=columns)
    for _, need_item in need_item_df_.iterrows():
        base = need_item["base"]
        item_df_ = item_df[item_df["base"] == base]
        rare = need_item["rare"]
        total_item_df.loc[total_item_df["ベースアイテム"] == base, "曜日"] = need_item["week"]
        total_item_df.loc[total_item_df["ベースアイテム"] == base, f"必要レア{rare}"] = need_item["必要数"]
        for _, item in item_df_.iterrows():
            rare = item["rare"]
            total_item_df.loc[total_item_df["ベースアイテム"] == base, f"所持レア{rare}"] = item["num"]
    total_item_df["所持数"] = (
        total_item_df["所持レア1"]
        + 3 * total_item_df["所持レア2"]
        + 9 * total_item_df["所持レア3"]
        + 27 * total_item_df["所持レア4"]
    )
    total_item_df["必要数"] = (
        total_item_df["必要レア1"]
        + 3 * total_item_df["必要レア2"]
        + 9 * total_item_df["必要レア3"]
        + 27 * total_item_df["必要レア4"]
    )
    total_item_df["差分"] = total_item_df["必要数"] - total_item_df["所持数"]
    total_item_df.loc[total_item_df["差分"] < 0, "差分"] = 0
    return total_item_df


def load_total_item_df(need_filter: bool = False) -> DataFrame:
    item_df = get_item_df()
    need_item_df = load_calc_item_df()
    total_item_df = _calc_total_item(item_df, need_item_df)
    if need_filter:
        total_item_df = total_item_df[total_item_df["差分"] > 0]
    return total_item_df


def _get_total_item_diff(old_df: DataFrame, new_df: DataFrame) -> DataFrame:
    drop_columns = ["所持数", "必要数", "差分", "必要レア1", "必要レア2", "必要レア3", "必要レア4", "曜日"]
    old_df = old_df.drop(columns=drop_columns)
    new_df = new_df.drop(columns=drop_columns)
    diff_df = old_df.merge(new_df, on="ベースアイテム", how="inner", suffixes=("_old", "_new"))
    diff_df = diff_df[
        (diff_df["所持レア1_old"] != diff_df["所持レア1_new"])
        | (diff_df["所持レア2_old"] != diff_df["所持レア2_new"])
        | (diff_df["所持レア3_old"] != diff_df["所持レア3_new"])
        | (diff_df["所持レア4_old"] != diff_df["所持レア4_new"])
    ]
    diff_df = diff_df.drop(columns=["所持レア1_old", "所持レア2_old", "所持レア3_old", "所持レア4_old"])
    diff_df = diff_df.rename(
        columns={
            "所持レア1_new": "1",
            "所持レア2_new": "2",
            "所持レア3_new": "3",
            "所持レア4_new": "4",
        }
    )
    return diff_df


def _update_total_item(diff_df: DataFrame, item_df: DataFrame) -> None:
    num_list: list[list[int]] = list()
    for base, rare1, rare2, rare3, rare4 in diff_df.values:
        base_df = item_df[item_df["base"] == base]
        rare1_df = base_df[base_df["rare"] == 1]
        rare2_df = base_df[base_df["rare"] == 2]
        rare3_df = base_df[base_df["rare"] == 3]
        rare4_df = base_df[base_df["rare"] == 4]
        if not rare1_df.empty:
            num_list.append([rare1_df.iloc[0]["id"], rare1])
        if not rare2_df.empty:
            num_list.append([rare2_df.iloc[0]["id"], rare2])
        if not rare3_df.empty:
            num_list.append([rare3_df.iloc[0]["id"], rare3])
        if not rare4_df.empty:
            num_list.append([rare4_df.iloc[0]["id"], rare4])
    update_num(num_list)


def change_total_item_df(new_total_item_df: DataFrame, need_filter: bool = False) -> DataFrame:
    item_df = get_item_df()
    total_item_df = load_total_item_df()
    diff_df = _get_total_item_diff(total_item_df, new_total_item_df)
    _update_total_item(diff_df, item_df)
    return load_total_item_df(need_filter)
