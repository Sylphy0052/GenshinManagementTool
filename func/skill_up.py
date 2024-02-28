from cruds.chara import (
    update_chara_lv,
    update_chara_skill1,
    update_chara_skill2,
    update_chara_skill3,
)
from cruds.item import update_num
from cruds.weapon import update_weapon_lv
from func.chara import get_chara_df
from func.item import get_item_df
from func.weapon import get_player_weapon_df
from settings import (
    ELEMENT_STONE,
    NEED_LV_ITEM,
    NEED_SKILL_ITEM,
    WEAPON3_LV_ITEM,
    WEAPON4_LV_ITEM,
    WEAPON5_LV_ITEM,
)


def lvup_lv(chara_name: str) -> None:
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_lv = int(chara["level"])
    to_lv = min([lv for lv in list(NEED_LV_ITEM.keys()) if lv >= current_lv])
    item_df = get_item_df()
    for item_type, (rare, num) in NEED_LV_ITEM[to_lv].items():
        if item_type == "stone":
            item = ELEMENT_STONE[chara["element"]]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        to_num = int(item_s["num"]) - num
        update_num([[item_s["id"], to_num]])
    lv = to_lv + 1
    update_chara_lv([[chara["id"], lv]])


def lvup_skill1(chara_name: str) -> None:
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_lv = int(chara["skill1"])
    to_lv = current_lv + 1
    item_df = get_item_df()
    for item_type, (rare, num) in NEED_SKILL_ITEM[to_lv].items():
        if item_type == "special":
            item = item_df[item_df["item_type"] == item_type].iloc[0]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        to_num = int(item_s["num"]) - num
        update_num([[item_s["id"], to_num]])
    lv = to_lv + 1
    update_chara_skill1([[chara["id"], lv]])


def lvup_skill2(chara_name: str) -> None:
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_lv = int(chara["skill2"])
    to_lv = current_lv + 1
    item_df = get_item_df()
    for item_type, (rare, num) in NEED_SKILL_ITEM[to_lv].items():
        if item_type == "special":
            item = item_df[item_df["item_type"] == item_type].iloc[0]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        to_num = int(item_s["num"]) - num
        update_num([[item_s["id"], to_num]])
    lv = to_lv + 1
    update_chara_skill2([[chara["id"], lv]])


def lvup_skill3(chara_name: str) -> None:
    chara_df = get_chara_df()
    chara = chara_df[chara_df["name"] == chara_name].iloc[0]
    current_lv = int(chara["skill3"])
    to_lv = current_lv + 1
    item_df = get_item_df()
    for item_type, (rare, num) in NEED_SKILL_ITEM[to_lv].items():
        if item_type == "special":
            item = item_df[item_df["item_type"] == item_type].iloc[0]
        else:
            item = chara[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        to_num = int(item_s["num"]) - num
        update_num([[item_s["id"], to_num]])
    lv = to_lv + 1
    update_chara_skill3([[chara["id"], lv]])


def lvup_weapon_lv(weapon_name: str) -> None:
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
        return
    to_lv = min([lv for lv in list(weapon_lv_item.keys()) if lv >= current_lv])
    item_df = get_item_df()
    for item_type, (rare, num) in weapon_lv_item[to_lv].items():
        item = weapon[item_type]
        item_s = item_df[(item_df["base"] == item) & (item_df["rare"] == rare)].iloc[0]
        to_num = int(item_s["num"]) - num
        update_num([[item_s["id"], to_num]])
    lv = to_lv + 1
    update_weapon_lv([[weapon["id"], lv]])
