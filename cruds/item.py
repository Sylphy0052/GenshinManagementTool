import logging

from pandas import DataFrame

from cruds.db import session as session_
from models.item import Item
from settings import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def create_item_data(item_datas: DataFrame) -> None:
    item_list: list[Item] = list()
    for _, item_data in item_datas.iterrows():
        item = Item(
            name=item_data["name"],
            item_type=item_data["item_type"],
            rare=item_data["rare"],
            base=item_data["base"],
            enemy=item_data["enemy"],
            week=item_data["week"],
        )
        item_list.append(item)
    with session_() as session:
        session.add_all(item_list)
        session.commit()


def read_item() -> list[Item]:
    with session_() as session:
        item_list = session.query(Item).all()
    return item_list  # type: ignore


def update_num(diff_list: list[list[int]]) -> None:
    with session_() as session:
        for idx, num in diff_list:
            item = session.query(Item).filter(Item.id == idx).first()
            try:
                if int(num) >= 0:
                    item.num = int(num)  # type: ignore
            except Exception as e:
                logger.error(e)
                continue
        session.commit()


def update_item_from_df(df: DataFrame) -> None:
    with session_() as session:
        for _, row in df.iterrows():
            item = session.query(Item).filter(Item.name == row["name"]).first()
            try:
                if int(row["num"]) >= 0:
                    item.num = int(row["num"])  # type: ignore
            except Exception as e:
                logger.error(e)
                continue
        session.commit()
