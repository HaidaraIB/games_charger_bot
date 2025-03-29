from telegram import InlineKeyboardButton
from common.lang_dicts import *
from common.constants import *
import models

def build_products_keyboard(lang: str):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["pubg"],
                callback_data="pubg",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["freefire"],
                callback_data="freefire",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["jawaker"],
                callback_data="jawaker",
            ),
        ],
    ]
    return keyboard


def build_groups_keyboard(product: str, lang: str):
    if product == "pubg":
        keboard = [
            [
                InlineKeyboardButton(
                    text=BUTTONS[lang]["uc_bundles"],
                    callback_data="uc_bundles",
                )
            ]
        ]
    elif product == "freefire":
        keboard = [
            [
                InlineKeyboardButton(
                    text=BUTTONS[lang]["diamonds"],
                    callback_data="diamonds",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=BUTTONS[lang]["memberships"],
                    callback_data="memberships",
                ),
            ],
        ]
    elif product == "jawaker":
        keboard = [
            [
                InlineKeyboardButton(
                    text=BUTTONS[lang]["tokens"],
                    callback_data="tokens",
                )
            ]
        ]
    return keboard


def filter_by_group(products: list[dict], group: str):
    groups_dict = {
        "tokens": JAWAKER_TOKENS_IDS,
        "uc_bundles": PUBG_UC_BUNDLES,
        "diamonds": FREEFIRE_DIAMONDS,
        "memberships": FREEFIRE_MEMBERSHIPS,
    }
    return [product for product in products if product.get("id") in groups_dict[group]]


def filter_by_id(products: list[dict], category_id: int):
    for product in products:
        if product["id"] == category_id:
            return product


