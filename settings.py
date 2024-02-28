import logging
import os

# Log Settings
LOG_DIR = os.path.join("logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "app.log")
MAX_BYTES = 10**6  # 1MB
BACKUP_COUNT = 100
LOG_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s"
# LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.INFO
LOGGER_NAME = "app"

# DB Settings
DB_PATH = "db.sqlite"
DB_URL = f"sqlite:///{DB_PATH}"
SQL_ECHO = LOG_LEVEL == logging.DEBUG

# CSV
CSV_DIR = os.path.join("csv_datas")
CHARA_PATH = os.path.join(CSV_DIR, "chara.csv")
WEAPON_PATH = os.path.join(CSV_DIR, "weapon.csv")
ITEM_PATH = os.path.join(CSV_DIR, "item.csv")

# FILE
FILE_DIR = os.path.join("save_files")
os.makedirs(FILE_DIR, exist_ok=True)

# 定数
CHARA_RENAME_COL = {
    "name": "キャラ名",
    "rare": "レア",
    "element": "属性",
    "level": "Lv",
    "t_level": "目標Lv",
    "skill1": "通常攻撃",
    "skill2": "スキル",
    "skill3": "元素爆発",
    "t_skill1": "目標:通常攻撃",
    "t_skill2": "目標:スキル",
    "t_skill3": "目標:元素爆発",
    "specialty": "特産品",
    "enemy": "敵",
    "boss": "ボス",
    "book": "本",
    "weekly_boss": "週ボス",
    "is_get": "入手",
    "is_calc": "計算対象",
}
MASTER_WEAPON_RENAME_COL = {
    "name": "武器名",
    "rare": "レア",
    "weapon_type": "武器種",
    "weapon": "武器素材",
    "enemy1": "敵1",
    "enemy2": "敵2",
}
WEAPON_RENAME_COL = {
    "name": "武器名",
    "rare": "レア",
    "weapon_type": "武器種",
    "level": "Lv",
    "t_level": "目標Lv",
    "refine": "精錬",
    "weapon": "武器素材",
    "enemy1": "敵1",
    "enemy2": "敵2",
    "is_get": "入手",
    "is_calc": "計算対象",
}
ITEM_RENAME_COL = {
    "name": "アイテム名",
    "item_type": "種類",
    "rare": "レア",
    "enemy": "敵",
    "week": "曜日",
    "num": "所持数",
}
ITEM_RENAME_VALUES = {
    "種類": {
        "field": "敵",
        "weekly_boss": "週ボス",
        "boss": "ボス",
        "stone": "石",
        "book": "本",
        "special": "特別",
        "weapon": "突破素材",
        "specialty": "特産品",
    }
}

NEED_LV_ITEM = {
    20: {"specialty": (1, 3), "enemy": (1, 3), "stone": (1, 1)},
    40: {"specialty": (1, 10), "enemy": (1, 15), "boss": (1, 2), "stone": (2, 3)},
    50: {"specialty": (1, 20), "enemy": (2, 12), "boss": (1, 4), "stone": (2, 6)},
    60: {"specialty": (1, 30), "enemy": (2, 18), "boss": (1, 8), "stone": (3, 3)},
    70: {"specialty": (1, 45), "enemy": (3, 12), "boss": (1, 12), "stone": (3, 6)},
    80: {"specialty": (1, 60), "enemy": (3, 24), "boss": (1, 20), "stone": (4, 6)},
}
NEED_SKILL_ITEM = {
    2: {"enemy": (1, 6), "book": (1, 3)},
    3: {"enemy": (2, 3), "book": (2, 2)},
    4: {"enemy": (2, 4), "book": (2, 4)},
    5: {"enemy": (2, 6), "book": (2, 6)},
    6: {"enemy": (2, 9), "book": (2, 9)},
    7: {"enemy": (3, 4), "book": (3, 4), "weekly_boss": (1, 1)},
    8: {"enemy": (3, 6), "book": (3, 6), "weekly_boss": (1, 1)},
    9: {"enemy": (3, 9), "book": (3, 12), "weekly_boss": (1, 2)},
    10: {"enemy": (3, 12), "book": (3, 16), "weekly_boss": (1, 2), "special": (1, 1)},
}
WEAPON3_LV_ITEM = {
    20: {"weapon": (1, 2), "enemy1": (1, 1), "enemy2": (1, 2)},
    40: {"weapon": (2, 2), "enemy1": (1, 5), "enemy2": (1, 8)},
    50: {"weapon": (2, 4), "enemy1": (2, 4), "enemy2": (2, 4)},
    60: {"weapon": (3, 2), "enemy1": (2, 6), "enemy2": (2, 8)},
    70: {"weapon": (3, 4), "enemy1": (3, 4), "enemy2": (3, 6)},
    80: {"weapon": (4, 3), "enemy1": (3, 8), "enemy2": (3, 12)},
}
WEAPON4_LV_ITEM = {
    20: {"weapon": (1, 3), "enemy1": (1, 2), "enemy2": (1, 3)},
    40: {"weapon": (2, 3), "enemy1": (1, 8), "enemy2": (1, 12)},
    50: {"weapon": (2, 6), "enemy1": (2, 6), "enemy2": (2, 6)},
    60: {"weapon": (3, 3), "enemy1": (2, 9), "enemy2": (2, 12)},
    70: {"weapon": (3, 6), "enemy1": (3, 6), "enemy2": (3, 9)},
    80: {"weapon": (4, 4), "enemy1": (3, 12), "enemy2": (3, 18)},
}
WEAPON5_LV_ITEM = {
    20: {"weapon": (1, 5), "enemy1": (1, 3), "enemy2": (1, 5)},
    40: {"weapon": (2, 5), "enemy1": (1, 12), "enemy2": (1, 18)},
    50: {"weapon": (2, 9), "enemy1": (2, 9), "enemy2": (2, 9)},
    60: {"weapon": (3, 5), "enemy1": (2, 14), "enemy2": (2, 18)},
    70: {"weapon": (3, 9), "enemy1": (3, 9), "enemy2": (3, 14)},
    80: {"weapon": (4, 6), "enemy1": (3, 18), "enemy2": (3, 27)},
}
ELEMENT_STONE = {
    "炎": "アゲート",
    "水": "ラピスラズリ",
    "雷": "アメシスト",
    "氷": "アイスクリスタル",
    "風": "ターコイズ",
    "岩": "トパーズ",
    "草": "エメラルド",
}
