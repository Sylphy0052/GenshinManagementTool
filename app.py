import logging
import os
import webbrowser

import gradio as gr

from cruds.migrate import create_db, reset_db
from func.calc_item import (
    change_calc_item_df,
    change_total_item_df,
    load_calc_item_df,
    load_total_item_df,
)
from func.chara import (
    change_calc_target_chara_df,
    change_player_chara_df,
    load_calc_target_chara_df,
    load_chara_list_df,
    load_player_chara_df,
)
from func.create_selection import (
    change_lvup_value,
    change_lvup_weapon_value,
    change_skill1_value,
    change_skill2_value,
    change_skill3_value,
    get_get_chara_list,
    load_lvup_lv_df,
    load_lvup_skill1_df,
    load_lvup_skill2_df,
    load_lvup_skill3_df,
    load_lvup_weapon_df,
)
from func.file import (
    download_chara_csv,
    download_item_csv,
    download_weapon_csv,
    upload_chara_csv,
    upload_item_csv,
    upload_weapon_csv,
)
from func.item import change_player_item_df, load_item_list_df, load_player_item_df
from func.skill_up import lvup_lv, lvup_skill1, lvup_skill2, lvup_skill3, lvup_weapon_lv
from func.weapon import (
    add_weapon,
    change_calc_weapon_df,
    change_player_weapon_df,
    delete_weapon,
    get_get_weapon_detail_list,
    get_weapon_detail_list,
    get_weapon_list,
    load_calc_weapon_df,
    load_player_weapon_df,
    load_weapon_list_df,
)
from settings import (
    BACKUP_COUNT,
    FILE_DIR,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_PATH,
    LOGGER_NAME,
    MAX_BYTES,
)

# ログ設定
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter(LOG_FORMAT)
rh = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)  # type: ignore
rh.setLevel(LOG_LEVEL)
rh.setFormatter(formatter)
logger.addHandler(rh)

# DB作成
create_db()
reset_db()

app = gr.Blocks(title="原神素材計算機")
with app:
    gr.Markdown("# 原神素材計算機")
    with gr.Tab("キャラクター"):
        with gr.Tab("一覧"):
            with gr.Row():
                chara_list_rare_filter = gr.Dropdown(
                    choices=["", "4", "5"],
                    value="",
                    label="レア",
                )
                chara_list_element_filter = gr.Dropdown(
                    choices=["", "炎", "水", "氷", "雷", "風", "岩", "草"],
                    value="",
                    label="属性",
                )
                with gr.Column():
                    chara_list_get_filter = gr.Checkbox(label="入手済みのみ")
                    chara_list_calc_filter = gr.Checkbox(label="計算対象のみ")
            chara_list_df = gr.DataFrame()
        with gr.Tab("キャラ編集"):
            with gr.Row():
                player_chara_rare_filter = gr.Dropdown(
                    choices=["", "4", "5"],
                    value="",
                    label="レア",
                )
                player_chara_element_filter = gr.Dropdown(
                    choices=["", "炎", "水", "氷", "雷", "風", "岩", "草"],
                    value="",
                    label="属性",
                )
                with gr.Column():
                    player_chara_get_filter = gr.Checkbox(label="入手済みのみ")
                    player_chara_calc_filter = gr.Checkbox(label="計算対象のみ")
            player_chara_edit_button = gr.Button("更新")
            player_chara_df = gr.DataFrame(interactive=True)
        with gr.Tab("計算"):
            with gr.Row():
                calc_target_chara_rare_filter = gr.Dropdown(
                    choices=["", "4", "5"],
                    value="",
                    label="レア",
                )
                calc_target_chara_element_filter = gr.Dropdown(
                    choices=["", "炎", "水", "氷", "雷", "風", "岩", "草"],
                    value="",
                    label="属性",
                )
                with gr.Column():
                    calc_target_chara_get_filter = gr.Checkbox(label="入手済みのみ")
                    calc_target_chara_calc_filter = gr.Checkbox(label="計算対象のみ")
            calc_target_chara_edit_button = gr.Button("更新")
            calc_target_chara_df = gr.DataFrame(
                label="計算対象キャラ",
                show_label=True,
                interactive=True,
            )
        with gr.Tab("キャラ突破"):
            chara_lvup_chara = gr.Dropdown(choices=get_get_chara_list(), value="", label="キャラ")  # type: ignore
            with gr.Row():
                chara_lvup_lv_button = gr.Button("Lv Up")
                chara_lvup_skill1_button = gr.Button("通常攻撃 Up")
                chara_lvup_skill2_button = gr.Button("スキル Up")
                chara_lvup_skill3_button = gr.Button("元素爆発 Up")
            with gr.Accordion(label="Lv素材", open=False):
                lvup_chara_lv_df = gr.DataFrame()
            with gr.Accordion(label="通常攻撃素材", open=False):
                lvup_chara_skill1_df = gr.DataFrame()
            with gr.Accordion(label="スキル素材", open=False):
                lvup_chara_skill2_df = gr.DataFrame()
            with gr.Accordion(label="元素爆発素材", open=False):
                lvup_chara_skill3_df = gr.DataFrame()
    with gr.Tab("武器"):
        with gr.Tab("一覧"):
            with gr.Row():
                weapon_list_rare_filter = gr.Dropdown(
                    choices=["", "3", "4", "5"],
                    value="",
                    label="レア",
                )
                weapon_list_type_filter = gr.Dropdown(
                    choices=["", "片手剣", "両手剣", "槍", "法器", "弓"],
                    value="",
                    label="武器種",
                )
            weapon_list_df = gr.DataFrame()
        with gr.Tab("所持武器"):
            with gr.Row():
                player_weapon_rare_filter = gr.Dropdown(
                    choices=["", "3", "4", "5"],
                    value="",
                    label="レア",
                )
                player_weapon_type_filter = gr.Dropdown(
                    choices=["", "片手剣", "両手剣", "槍", "法器", "弓"],
                    value="",
                    label="武器種",
                )
                with gr.Column():
                    player_weapon_get_filter = gr.Checkbox(label="入手済みのみ")
                    player_weapon_calc_filter = gr.Checkbox(label="計算対象のみ")
            player_weapon_edit_button = gr.Button("更新")
            player_weapon_df = gr.DataFrame(interactive=True)
        with gr.Tab("武器追加"):
            with gr.Row():
                add_weapon_rare_filter = gr.Dropdown(
                    choices=["", "3", "4", "5"],
                    value="",
                    label="レア",
                )
                add_weapon_type_filter = gr.Dropdown(
                    choices=["", "片手剣", "両手剣", "槍", "法器", "弓"],
                    value="",
                    label="武器種",
                )
            add_weapon_name = gr.Dropdown(
                choices=get_weapon_list(), value="", label="武器", interactive=True  # type: ignore
            )
            add_weapon_lv = gr.Slider(minimum=1, maximum=90, step=1, label="レベル", interactive=True)
            add_weapon_refine = gr.Slider(minimum=1, maximum=5, step=1, label="精錬ランク", interactive=True)
            with gr.Row():
                add_weapon_get = gr.Checkbox(label="入手済み")
                add_weapon_calc = gr.Checkbox(label="計算対象")
            add_weapon_button = gr.Button("追加")
        with gr.Tab("武器削除"):
            with gr.Row():
                delete_weapon_rare_filter = gr.Dropdown(
                    choices=["", "3", "4", "5"],
                    value="",
                    label="レア",
                )
                delete_weapon_type_filter = gr.Dropdown(
                    choices=["", "片手剣", "両手剣", "槍", "法器", "弓"],
                    value="",
                    label="武器種",
                )
            delete_weapon_name = gr.Dropdown(
                choices=get_weapon_detail_list(), value="", label="武器", interactive=True  # type: ignore
            )
            delete_weapon_button = gr.Button("削除")
        with gr.Tab("計算"):
            with gr.Row():
                calc_weapon_rare_filter = gr.Dropdown(
                    choices=["", "3", "4", "5"],
                    value="",
                    label="レア",
                )
                calc_weapon_type_filter = gr.Dropdown(
                    choices=["", "片手剣", "両手剣", "槍", "法器", "弓"],
                    value="",
                    label="武器種",
                )
                with gr.Column():
                    calc_weapon_get_filter = gr.Checkbox(label="入手済みのみ")
                    calc_weapon_calc_filter = gr.Checkbox(label="計算対象のみ")
            calc_weapon_edit_button = gr.Button("更新")
            calc_weapon_df = gr.DataFrame(interactive=True)
        with gr.Tab("武器強化"):
            with gr.Row():
                lvup_weapon_rare_filter = gr.Dropdown(
                    choices=["", "3", "4", "5"],
                    value="",
                    label="レア",
                )
                lvup_weapon_type_filter = gr.Dropdown(
                    choices=["", "片手剣", "両手剣", "槍", "法器", "弓"],
                    value="",
                    label="武器種",
                )
            lvup_weapon = gr.Dropdown(choices=get_weapon_detail_list(), label="武器", interactive=True)  # type: ignore
            weapon_lvup_button = gr.Button("強化")
            with gr.Accordion(label="強化素材", open=False):
                lvup_weapon_df = gr.DataFrame()
    with gr.Tab("素材"):
        with gr.Tab("一覧"):
            item_list_filter = gr.Dropdown(
                choices=["", "敵", "週ボス", "ボス", "石", "本", "特別", "突破素材", "特産品"],
                value="",
                label="種類",
            )
            item_list_df = gr.DataFrame()
        with gr.Tab("所持"):
            player_item_filter = gr.Dropdown(
                choices=["", "敵", "週ボス", "ボス", "石", "本", "特別", "突破素材", "特産品"],
                value="",
                label="種類",
            )
            player_item_edit_button = gr.Button("更新")
            player_item_df = gr.DataFrame(interactive=True)
        with gr.Tab("計算"):
            need_item_need_filter = gr.Checkbox(label="不足のみ")
            need_item_edit_button = gr.Button("更新")
            need_item_df = gr.DataFrame(interactive=True)
            total_item_need_filter = gr.Checkbox(label="不足のみ")
            total_item_edit_button = gr.Button("更新")
            total_item_df = gr.DataFrame(interactive=True)
    with gr.Tab("File"):
        with gr.Row():
            chara_dl_button = gr.Button(
                "キャラデータダウンロード", link=f"/file={os.path.join(FILE_DIR, 'chara.csv')}"
            )
            weapon_dl_button = gr.Button(
                "武器データダウンロード", link=f"/file={os.path.join(FILE_DIR, 'weapon.csv')}"
            )
            item_dl_button = gr.Button("素材データダウンロード", link=f"/file={os.path.join(FILE_DIR, 'item.csv')}")
        with gr.Row():
            chara_upload_file = gr.UploadButton("キャラデータアップロード", file_types=[".csv"])
            weapon_upload_file = gr.UploadButton("武器データアップロード", file_types=[".csv"])
            item_upload_file = gr.UploadButton("素材データアップロード", file_types=[".csv"])
    # イベントリスナー
    # キャラ一覧フィルタ
    chara_list_rare_filter.change(
        load_chara_list_df,
        inputs=[chara_list_rare_filter, chara_list_element_filter, chara_list_get_filter, chara_list_calc_filter],
        outputs=chara_list_df,
    )
    chara_list_element_filter.change(
        load_chara_list_df,
        inputs=[chara_list_rare_filter, chara_list_element_filter, chara_list_get_filter, chara_list_calc_filter],
        outputs=chara_list_df,
    )
    chara_list_get_filter.change(
        load_chara_list_df,
        inputs=[chara_list_rare_filter, chara_list_element_filter, chara_list_get_filter, chara_list_calc_filter],
        outputs=chara_list_df,
    )
    chara_list_calc_filter.change(
        load_chara_list_df,
        inputs=[chara_list_rare_filter, chara_list_element_filter, chara_list_get_filter, chara_list_calc_filter],
        outputs=chara_list_df,
    )
    # キャラ編集フィルタ
    player_chara_rare_filter.change(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    )
    player_chara_element_filter.change(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    )
    player_chara_get_filter.change(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    )
    player_chara_calc_filter.change(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    )
    # キャラ編集
    player_chara_edit_button.click(
        change_player_chara_df,
        inputs=[
            player_chara_df,
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    ).then(
        load_chara_list_df,
        inputs=[chara_list_rare_filter, chara_list_element_filter, chara_list_get_filter, chara_list_calc_filter],
        outputs=chara_list_df,
    ).then(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    ).then(
        lambda: gr.update(choices=get_get_chara_list()), outputs=chara_lvup_chara
    ).then(
        change_lvup_value, inputs=chara_lvup_chara, outputs=chara_lvup_lv_button
    ).then(
        change_skill1_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill1_button
    ).then(
        change_skill2_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill2_button
    ).then(
        change_skill3_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill3_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_chara_csv
    )
    # 計算対象キャラフィルタ
    calc_target_chara_rare_filter.change(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    )
    calc_target_chara_element_filter.change(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    )
    calc_target_chara_get_filter.change(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    )
    calc_target_chara_calc_filter.change(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    )
    # 計算対象キャラ編集
    calc_target_chara_edit_button.click(
        change_calc_target_chara_df,
        inputs=[
            calc_target_chara_df,
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    ).then(
        load_chara_list_df,
        inputs=[chara_list_rare_filter, chara_list_element_filter, chara_list_get_filter, chara_list_calc_filter],
        outputs=chara_list_df,
    ).then(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    ).then(
        lambda: gr.update(choices=get_get_chara_list()), outputs=chara_lvup_chara
    ).then(
        change_lvup_value, inputs=chara_lvup_chara, outputs=chara_lvup_lv_button
    ).then(
        change_skill1_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill1_button
    ).then(
        change_skill2_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill2_button
    ).then(
        change_skill3_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill3_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_chara_csv
    )
    # キャラ突破
    chara_lvup_chara.change(change_lvup_value, inputs=chara_lvup_chara, outputs=chara_lvup_lv_button).then(
        change_skill1_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill1_button
    ).then(change_skill2_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill2_button).then(
        change_skill3_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill3_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    )
    # 実行
    chara_lvup_lv_button.click(lvup_lv, inputs=chara_lvup_chara).then(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    ).then(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    ).then(
        change_lvup_value, inputs=chara_lvup_chara, outputs=chara_lvup_lv_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_player_item_df, inputs=player_item_filter, outputs=player_item_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_chara_csv
    ).then(
        download_item_csv
    )
    chara_lvup_skill1_button.click(lvup_skill1, inputs=chara_lvup_chara).then(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    ).then(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    ).then(
        change_skill1_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill1_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_player_item_df, inputs=player_item_filter, outputs=player_item_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_chara_csv
    ).then(
        download_item_csv
    )
    chara_lvup_skill2_button.click(lvup_skill2, inputs=chara_lvup_chara).then(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    ).then(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    ).then(
        change_skill2_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill2_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_player_item_df, inputs=player_item_filter, outputs=player_item_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_chara_csv
    ).then(
        download_item_csv
    )
    chara_lvup_skill3_button.click(lvup_skill3, inputs=chara_lvup_chara).then(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    ).then(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    ).then(
        change_skill3_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill3_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_player_item_df, inputs=player_item_filter, outputs=player_item_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_chara_csv
    ).then(
        download_item_csv
    )

    # 武器一覧フィルタ
    weapon_list_rare_filter.change(
        load_weapon_list_df,
        inputs=[weapon_list_rare_filter, weapon_list_type_filter],
        outputs=weapon_list_df,
    )
    weapon_list_type_filter.change(
        load_weapon_list_df,
        inputs=[weapon_list_rare_filter, weapon_list_type_filter],
        outputs=weapon_list_df,
    )
    # 所持武器フィルタ
    player_weapon_rare_filter.change(
        load_player_weapon_df,
        inputs=[
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    )
    player_weapon_type_filter.change(
        load_player_weapon_df,
        inputs=[
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    )
    player_weapon_get_filter.change(
        load_player_weapon_df,
        inputs=[
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    )
    player_weapon_calc_filter.change(
        load_player_weapon_df,
        inputs=[
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    )
    # 所持武器編集
    player_weapon_edit_button.click(
        change_player_weapon_df,
        inputs=[
            player_weapon_df,
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_weapon_detail_list(x, y)),
        inputs=[delete_weapon_rare_filter, delete_weapon_type_filter],
        outputs=delete_weapon_name,
    ).then(
        lambda x, y: gr.update(choices=get_get_weapon_detail_list(x, y)),
        inputs=[lvup_weapon_rare_filter, lvup_weapon_type_filter],
        outputs=lvup_weapon,
    ).then(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_get_weapon_detail_list(x, y)),
        inputs=[lvup_weapon_rare_filter, lvup_weapon_type_filter],
        outputs=lvup_weapon,
    ).then(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_weapon_csv
    )
    # 武器追加フィルタ
    add_weapon_rare_filter.change(
        lambda x, y: gr.update(choices=get_weapon_list(x, y)),
        inputs=[add_weapon_rare_filter, add_weapon_type_filter],
        outputs=add_weapon_name,
    )
    add_weapon_type_filter.change(
        lambda x, y: gr.update(choices=get_weapon_list(x, y)),
        inputs=[add_weapon_rare_filter, add_weapon_type_filter],
        outputs=add_weapon_name,
    )
    # 武器追加
    add_weapon_button.click(
        add_weapon,
        inputs=[add_weapon_name, add_weapon_lv, add_weapon_refine, add_weapon_get, add_weapon_calc],
    ).then(
        lambda: gr.update(value=""),
        outputs=add_weapon_name,
    ).then(
        lambda: gr.update(value=1),
        outputs=add_weapon_lv,
    ).then(
        lambda: gr.update(value=1),
        outputs=add_weapon_refine,
    ).then(
        load_player_weapon_df,
        inputs=[
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_weapon_detail_list(x, y)),
        inputs=[delete_weapon_rare_filter, delete_weapon_type_filter],
        outputs=delete_weapon_name,
    ).then(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_get_weapon_detail_list(x, y)),
        inputs=[lvup_weapon_rare_filter, lvup_weapon_type_filter],
        outputs=lvup_weapon,
    ).then(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_weapon_csv
    )
    # 武器削除フィルタ
    delete_weapon_rare_filter.change(
        lambda x, y: gr.update(choices=get_weapon_detail_list(x, y)),
        inputs=[delete_weapon_rare_filter, delete_weapon_type_filter],
        outputs=delete_weapon_name,
    )
    delete_weapon_type_filter.change(
        lambda x, y: gr.update(choices=get_weapon_detail_list(x, y)),
        inputs=[delete_weapon_rare_filter, delete_weapon_type_filter],
        outputs=delete_weapon_name,
    )
    delete_weapon_button.click(delete_weapon, inputs=delete_weapon_name).then(
        load_player_weapon_df,
        inputs=[
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_weapon_detail_list(x, y)),
        inputs=[delete_weapon_rare_filter, delete_weapon_type_filter],
        outputs=delete_weapon_name,
    ).then(
        lambda: gr.update(value=""),
        outputs=delete_weapon_name,
    ).then(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_get_weapon_detail_list(x, y)),
        inputs=[lvup_weapon_rare_filter, lvup_weapon_type_filter],
        outputs=lvup_weapon,
    ).then(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_weapon_csv
    )
    # 武器計算フィルタ
    calc_weapon_rare_filter.change(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    )
    calc_weapon_type_filter.change(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    )
    calc_weapon_get_filter.change(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    )
    calc_weapon_calc_filter.change(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    )
    # 武器計算編集
    calc_weapon_edit_button.click(
        change_calc_weapon_df,
        inputs=[
            calc_weapon_df,
            calc_weapon_rare_filter,
            calc_weapon_type_filter,
            calc_weapon_get_filter,
            calc_weapon_calc_filter,
        ],
        outputs=calc_weapon_df,
    ).then(
        load_player_weapon_df,
        inputs=[
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_weapon_csv
    )
    # 武器強化フィルタ
    lvup_weapon_rare_filter.change(
        lambda x, y: gr.update(choices=get_get_weapon_detail_list(x, y)),
        inputs=[lvup_weapon_rare_filter, lvup_weapon_type_filter],
        outputs=lvup_weapon,
    )
    lvup_weapon_type_filter.change(
        lambda x, y: gr.update(choices=get_get_weapon_detail_list(x, y)),
        inputs=[lvup_weapon_rare_filter, lvup_weapon_type_filter],
        outputs=lvup_weapon,
    )
    # 武器強化変更
    lvup_weapon.change(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    )
    # 武器強化
    weapon_lvup_button.click(
        lvup_weapon_lv,
        inputs=lvup_weapon,
    ).then(
        load_player_weapon_df,
        inputs=[
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_weapon_detail_list(x, y)),
        inputs=[delete_weapon_rare_filter, delete_weapon_type_filter],
        outputs=delete_weapon_name,
    ).then(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_get_weapon_detail_list(x, y)),
        inputs=[lvup_weapon_rare_filter, lvup_weapon_type_filter],
        outputs=lvup_weapon,
    ).then(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    ).then(
        load_player_item_df, inputs=player_item_filter, outputs=player_item_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_weapon_csv
    ).then(
        download_item_csv
    )

    # 素材一覧フィルタ
    item_list_filter.change(load_item_list_df, inputs=item_list_filter, outputs=item_list_df)
    # 所持素材フィルタ
    player_item_filter.change(load_player_item_df, inputs=player_item_filter, outputs=player_item_df)
    # 所持素材編集
    player_item_edit_button.click(change_player_item_df, inputs=player_item_df, outputs=player_item_df).then(
        change_lvup_value, inputs=chara_lvup_chara, outputs=chara_lvup_lv_button
    ).then(change_skill1_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill1_button).then(
        change_skill2_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill2_button
    ).then(
        change_skill3_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill3_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    ).then(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_item_csv
    )
    # 素材計算フィルタ
    need_item_need_filter.change(load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df)
    # 素材計算編集
    need_item_edit_button.click(
        change_calc_item_df, inputs=[need_item_df, need_item_need_filter], outputs=need_item_df
    ).then(change_lvup_value, inputs=chara_lvup_chara, outputs=chara_lvup_lv_button).then(
        change_skill1_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill1_button
    ).then(
        change_skill2_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill2_button
    ).then(
        change_skill3_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill3_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    ).then(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    ).then(
        load_player_item_df, inputs=player_item_filter, outputs=player_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_item_csv
    )
    # 合計素材計算フィルタ
    total_item_need_filter.change(load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df)
    # 合計素材計算編集
    total_item_edit_button.click(
        change_total_item_df, inputs=[total_item_df, total_item_need_filter], outputs=total_item_df
    ).then(change_lvup_value, inputs=chara_lvup_chara, outputs=chara_lvup_lv_button).then(
        change_skill1_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill1_button
    ).then(
        change_skill2_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill2_button
    ).then(
        change_skill3_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill3_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    ).then(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    ).then(
        load_player_item_df, inputs=player_item_filter, outputs=player_item_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        download_item_csv
    )
    # File
    # キャラファイルアップロード
    chara_upload_file.upload(upload_chara_csv, inputs=chara_upload_file).then(
        load_chara_list_df,
        inputs=[chara_list_rare_filter, chara_list_element_filter, chara_list_get_filter, chara_list_calc_filter],
        outputs=chara_list_df,
    ).then(
        load_player_chara_df,
        inputs=[
            player_chara_rare_filter,
            player_chara_element_filter,
            player_chara_get_filter,
            player_chara_calc_filter,
        ],
        outputs=player_chara_df,
    ).then(
        load_calc_target_chara_df,
        inputs=[
            calc_target_chara_rare_filter,
            calc_target_chara_element_filter,
            calc_target_chara_get_filter,
            calc_target_chara_calc_filter,
        ],
        outputs=calc_target_chara_df,
    ).then(
        lambda: gr.update(choices=get_get_chara_list()), outputs=chara_lvup_chara
    ).then(
        change_lvup_value, inputs=chara_lvup_chara, outputs=chara_lvup_lv_button
    ).then(
        change_skill1_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill1_button
    ).then(
        change_skill2_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill2_button
    ).then(
        change_skill3_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill3_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_chara_csv
    )

    # 武器ファイルアップロード
    weapon_upload_file.upload(upload_weapon_csv, inputs=weapon_upload_file).then(
        load_player_weapon_df,
        inputs=[
            player_weapon_rare_filter,
            player_weapon_type_filter,
            player_weapon_get_filter,
            player_weapon_calc_filter,
        ],
        outputs=player_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_weapon_detail_list(x, y)),
        inputs=[delete_weapon_rare_filter, delete_weapon_type_filter],
        outputs=delete_weapon_name,
    ).then(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    ).then(
        lambda x, y: gr.update(choices=get_get_weapon_detail_list(x, y)),
        inputs=[lvup_weapon_rare_filter, lvup_weapon_type_filter],
        outputs=lvup_weapon,
    ).then(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    )

    # 素材ファイルアップロード
    item_upload_file.upload(upload_item_csv, inputs=item_upload_file).then(
        change_lvup_value, inputs=chara_lvup_chara, outputs=chara_lvup_lv_button
    ).then(change_skill1_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill1_button).then(
        change_skill2_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill2_button
    ).then(
        change_skill3_value, inputs=chara_lvup_chara, outputs=chara_lvup_skill3_button
    ).then(
        load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df
    ).then(
        load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df
    ).then(
        load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df
    ).then(
        load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df
    ).then(
        load_calc_weapon_df,
        inputs=[calc_weapon_rare_filter, calc_weapon_type_filter, calc_weapon_get_filter, calc_weapon_calc_filter],
        outputs=calc_weapon_df,
    ).then(
        change_lvup_weapon_value,
        inputs=lvup_weapon,
        outputs=weapon_lvup_button,
    ).then(
        load_lvup_weapon_df,
        inputs=lvup_weapon,
        outputs=lvup_weapon_df,
    ).then(
        load_player_item_df, inputs=player_item_filter, outputs=player_item_df
    ).then(
        load_calc_item_df, inputs=need_item_need_filter, outputs=need_item_df
    ).then(
        load_total_item_df, inputs=total_item_need_filter, outputs=total_item_df
    ).then(
        download_item_csv
    )

    # 初回データ読み込み
    app.load(load_chara_list_df, outputs=chara_list_df)
    app.load(load_player_chara_df, outputs=player_chara_df)
    app.load(load_calc_target_chara_df, outputs=calc_target_chara_df)
    app.load(load_lvup_lv_df, inputs=chara_lvup_chara, outputs=lvup_chara_lv_df)
    app.load(load_lvup_skill1_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill1_df)
    app.load(load_lvup_skill2_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill2_df)
    app.load(load_lvup_skill3_df, inputs=chara_lvup_chara, outputs=lvup_chara_skill3_df)
    app.load(load_weapon_list_df, outputs=weapon_list_df)
    app.load(load_player_weapon_df, outputs=player_weapon_df)
    app.load(load_calc_weapon_df, outputs=calc_weapon_df)
    app.load(load_item_list_df, outputs=item_list_df)
    app.load(load_player_item_df, outputs=player_item_df)
    app.load(load_calc_item_df, outputs=need_item_df)
    app.load(load_total_item_df, outputs=total_item_df)
    app.load(download_chara_csv)
    app.load(download_item_csv)


if __name__ == "__main__":
    webbrowser.open("http://localhost:8000?__theme=dark", new=2, autoraise=True)
    app.queue()
    app.launch(server_name="0.0.0.0", server_port=8000, debug=LOG_LEVEL == logging.DEBUG, allowed_paths=[FILE_DIR])
