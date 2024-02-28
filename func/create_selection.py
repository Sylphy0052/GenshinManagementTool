from typing import Any

import gradio as gr
from pandas import DataFrame

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

ITEM_COLUMNS = ["id", "アイテム名", "所持数", "必要数", "差分", "種類", "レア", "敵", "曜日"]


def load_lvup_lv_df(chara_name: str) -> DataFrame:
    if chara_name == "":
        return DataFrame(columns=ITEM_COLUMNS)
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_lv = int(chara["level"])
    lv_list = [lv for lv in list(NEED_LV_ITEM.keys()) if lv >= current_lv]
    if len(lv_list) == 0:
        return DataFrame(columns=ITEM_COLUMNS)
    to_lv = min(lv_list)
    item_df = get_item_df()
    df_values = list()
    for item_type, (rare, num) in NEED_LV_ITEM[to_lv].items():
        if item_type == "stone":
            item = ELEMENT_STONE[chara["element"]]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        diff = num - int(item_s["num"]) if int(item_s["num"]) < num else 0
        df_values.append(
            [
                item_s["id"],
                item_s["name"],
                item_s["num"],
                num,
                diff,
                item_s["item_type"],
                item_s["rare"],
                item_s["enemy"],
                item_s["week"],
            ]
        )
    need_item_df = DataFrame(df_values, columns=ITEM_COLUMNS)
    need_item_df = need_item_df.replace(ITEM_RENAME_VALUES)
    return need_item_df


def load_lvup_skill1_df(chara_name: str) -> DataFrame:
    if chara_name == "":
        return DataFrame(columns=ITEM_COLUMNS)
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_skill = int(chara["skill1"])
    to_skill = current_skill + 1
    skill_list = [skill for skill in list(NEED_SKILL_ITEM.keys()) if skill > current_skill]
    if len(skill_list) == 0:
        return DataFrame(columns=ITEM_COLUMNS)
    item_df = get_item_df()
    df_values = list()
    for item_type, (rare, num) in NEED_SKILL_ITEM[to_skill].items():
        if item_type == "special":
            item = item_df["item_type" == item_type].iloc[0]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        diff = num - int(item_s["num"]) if int(item_s["num"]) < num else 0
        df_values.append(
            [
                item_s["id"],
                item_s["name"],
                item_s["num"],
                num,
                diff,
                item_s["item_type"],
                item_s["rare"],
                item_s["enemy"],
                item_s["week"],
            ]
        )
    need_item_df = DataFrame(df_values, columns=ITEM_COLUMNS)
    need_item_df = need_item_df.replace(ITEM_RENAME_VALUES)
    return need_item_df


def load_lvup_skill2_df(chara_name: str) -> DataFrame:
    if chara_name == "":
        return DataFrame(columns=ITEM_COLUMNS)
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_skill = int(chara["skill2"])
    to_skill = current_skill + 1
    skill_list = [skill for skill in list(NEED_SKILL_ITEM.keys()) if skill > current_skill]
    if len(skill_list) == 0:
        return DataFrame(columns=ITEM_COLUMNS)
    item_df = get_item_df()
    df_values = list()
    for item_type, (rare, num) in NEED_SKILL_ITEM[to_skill].items():
        if item_type == "special":
            item = item_df["item_type" == item_type].iloc[0]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        diff = num - int(item_s["num"]) if int(item_s["num"]) < num else 0
        df_values.append(
            [
                item_s["id"],
                item_s["name"],
                item_s["num"],
                num,
                diff,
                item_s["item_type"],
                item_s["rare"],
                item_s["enemy"],
                item_s["week"],
            ]
        )
    need_item_df = DataFrame(df_values, columns=ITEM_COLUMNS)
    need_item_df = need_item_df.replace(ITEM_RENAME_VALUES)
    return need_item_df


def load_lvup_skill3_df(chara_name: str) -> DataFrame:
    if chara_name == "":
        return DataFrame(columns=ITEM_COLUMNS)
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_skill = int(chara["skill3"])
    to_skill = current_skill + 1
    skill_list = [skill for skill in list(NEED_SKILL_ITEM.keys()) if skill > current_skill]
    if len(skill_list) == 0:
        return DataFrame(columns=ITEM_COLUMNS)
    item_df = get_item_df()
    df_values = list()
    for item_type, (rare, num) in NEED_SKILL_ITEM[to_skill].items():
        if item_type == "special":
            item = item_df["item_type" == item_type].iloc[0]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        diff = num - int(item_s["num"]) if int(item_s["num"]) < num else 0
        df_values.append(
            [
                item_s["id"],
                item_s["name"],
                item_s["num"],
                num,
                diff,
                item_s["item_type"],
                item_s["rare"],
                item_s["enemy"],
                item_s["week"],
            ]
        )
    need_item_df = DataFrame(df_values, columns=ITEM_COLUMNS)
    need_item_df = need_item_df.replace(ITEM_RENAME_VALUES)
    return need_item_df


def get_get_chara_list() -> list[str]:
    chara_df = get_chara_df()
    chara_df = chara_df[chara_df["is_get"] == "True"]
    chara_df = chara_df.sort_values("name")
    chara_list = [""]
    chara_list.extend(chara_df["name"].tolist())
    return chara_list


def change_lvup_value(chara_name: str) -> Any:
    if chara_name == "":
        return gr.update(value="Lv Up", interactive=False)
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_lv = int(chara["level"])
    lv_list = [lv for lv in list(NEED_LV_ITEM.keys()) if lv >= current_lv]
    if len(lv_list) == 0:
        return gr.update(value="Lv Up", interactive=False)
    to_lv = min(lv_list)
    item_df = get_item_df()
    for item_type, (rare, num) in NEED_LV_ITEM[to_lv].items():
        if item_type == "stone":
            item = ELEMENT_STONE[chara["element"]]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        if int(item_s["num"]) < num:
            return gr.update(value=f"Lv Up({min(lv_list)})", interactive=False)
    return gr.update(value=f"Lv Up({min(lv_list)})", interactive=True)


def change_skill1_value(chara_name: str) -> Any:
    if chara_name == "":
        return gr.update(value="通常攻撃 Up", interactive=False)
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_skill = int(chara["skill1"])
    to_skill = current_skill + 1
    skill_list = [skill for skill in list(NEED_SKILL_ITEM.keys()) if skill > current_skill]
    if len(skill_list) == 0:
        return gr.update(value="通常攻撃 Up", interactive=False)
    item_df = get_item_df()
    for item_type, (rare, num) in NEED_SKILL_ITEM[to_skill].items():
        if item_type == "special":
            item = item_df["item_type" == item_type].iloc[0]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        if int(item_s["num"]) < num:
            return gr.update(value=f"通常攻撃 Up({min(skill_list)})", interactive=False)
    return gr.update(value=f"通常攻撃 Up({min(skill_list)})", interactive=True)


def change_skill2_value(chara_name: str) -> Any:
    if chara_name == "":
        return gr.update(value="スキル Up", interactive=False)
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_skill = int(chara["skill2"])
    to_skill = current_skill + 1
    skill_list = [skill for skill in list(NEED_SKILL_ITEM.keys()) if skill > current_skill]
    if len(skill_list) == 0:
        return gr.update(value="スキル Up", interactive=False)
    item_df = get_item_df()
    for item_type, (rare, num) in NEED_SKILL_ITEM[to_skill].items():
        if item_type == "special":
            item = item_df["item_type" == item_type].iloc[0]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        if int(item_s["num"]) < num:
            return gr.update(value=f"スキル Up({min(skill_list)})", interactive=False)
    return gr.update(value=f"スキル Up({min(skill_list)})", interactive=True)


def change_skill3_value(chara_name: str) -> Any:
    if chara_name == "":
        return gr.update(value="元素爆発 Up", interactive=False)
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_skill = int(chara["skill3"])
    to_skill = current_skill + 1
    skill_list = [skill for skill in list(NEED_SKILL_ITEM.keys()) if skill > current_skill]
    if len(skill_list) == 0:
        return gr.update(value="元素爆発 Up", interactive=False)
    item_df = get_item_df()
    for item_type, (rare, num) in NEED_SKILL_ITEM[to_skill].items():
        if item_type == "special":
            item = item_df["item_type" == item_type].iloc[0]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        if int(item_s["num"]) < num:
            return gr.update(value=f"元素爆発 Up({min(skill_list)})", interactive=False)
    return gr.update(value=f"元素爆発 Up({min(skill_list)})", interactive=True)


def change_lvup_weapon_value(weapon_name: str) -> Any:
    if weapon_name == "":
        return gr.update(value="強化", interactive=False)
    if isinstance(weapon_name, list):
        return gr.update(value="強化", interactive=False)
    weapon_id = weapon_name.split(":")[0]
    weapon_df = get_player_weapon_df()
    weapon = weapon_df[weapon_df["id"] == weapon_id].iloc[0]
    current_lv = int(weapon["level"])
    weapon_rare = int(weapon["rare"])
    weapon_lv_item = dict()
    if weapon_rare == 5:
        weapon_lv_item = WEAPON5_LV_ITEM
    elif weapon_rare == 4:
        weapon_lv_item = WEAPON4_LV_ITEM
    elif weapon_rare == 3:
        weapon_lv_item = WEAPON3_LV_ITEM
    else:
        return gr.update(value="強化", interactive=False)
    lv_list = [lv for lv in list(weapon_lv_item.keys()) if lv >= current_lv]
    if len(lv_list) == 0:
        return gr.update(value="強化", interactive=False)
    to_lv = min(lv_list)
    item_df = get_item_df()
    for item_type, (rare, num) in weapon_lv_item[to_lv].items():
        item = weapon[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        if int(item_s["num"]) < num:
            return gr.update(value=f"強化({min(lv_list)})", interactive=False)
    return gr.update(value=f"強化({min(lv_list)})", interactive=True)


def load_lvup_weapon_df(weapon_name: str) -> DataFrame:
    if weapon_name == "":
        return DataFrame(columns=ITEM_COLUMNS)
    if isinstance(weapon_name, list):
        return DataFrame(columns=ITEM_COLUMNS)
    weapon_id = weapon_name.split(":")[0]
    weapon_df = get_player_weapon_df()
    weapon = weapon_df[weapon_df["id"] == weapon_id].iloc[0]
    current_lv = int(weapon["level"])
    weapon_rare = int(weapon["rare"])
    weapon_lv_item = dict()
    if weapon_rare == 5:
        weapon_lv_item = WEAPON5_LV_ITEM
    elif weapon_rare == 4:
        weapon_lv_item = WEAPON4_LV_ITEM
    elif weapon_rare == 3:
        weapon_lv_item = WEAPON3_LV_ITEM
    else:
        return DataFrame(columns=ITEM_COLUMNS)
    lv_list = [lv for lv in list(weapon_lv_item.keys()) if lv >= current_lv]
    if len(lv_list) == 0:
        return DataFrame(columns=ITEM_COLUMNS)
    to_lv = min(lv_list)
    item_df = get_item_df()
    df_values = list()
    for item_type, (rare, num) in weapon_lv_item[to_lv].items():
        item = weapon[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        diff = num - int(item_s["num"]) if int(item_s["num"]) < num else 0
        df_values.append(
            [
                item_s["id"],
                item_s["name"],
                item_s["num"],
                num,
                diff,
                item_s["item_type"],
                item_s["rare"],
                item_s["enemy"],
                item_s["week"],
            ]
        )
    need_item_df = DataFrame(df_values, columns=ITEM_COLUMNS)
    need_item_df = need_item_df.replace(ITEM_RENAME_VALUES)
    return need_item_df
