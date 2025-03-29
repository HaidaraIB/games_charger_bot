from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
)
from common.lang_dicts import *
import models


def build_user_keyboard(lang: str):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["products"],
                callback_data="products",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["account_info"],
                callback_data="account_info",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["settings"],
                callback_data="user_settings",
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def build_admin_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                text="إعدادات الآدمن ⚙️🎛",
                callback_data="admin_settings",
            )
        ],
        [
            InlineKeyboardButton(
                text="إعدادات وسائل الدفع 💳",
                callback_data="payment_methods_settings",
            )
        ],
        [
            InlineKeyboardButton(
                text="حظر/فك حظر 🔓🔒",
                callback_data="ban_unban",
            )
        ],
        [
            InlineKeyboardButton(
                text="إخفاء/إظهار كيبورد معرفة الآيديات 🪄",
                callback_data="hide_ids_keyboard",
            )
        ],
        [
            InlineKeyboardButton(
                text="المستخدمين 👤",
                callback_data="users",
            )
        ],
        [
            InlineKeyboardButton(
                text="رسالة جماعية 👥",
                callback_data="broadcast",
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def build_back_to_home_page_button(
    lang: str = models.Language.ARABIC.name, is_admin: bool = True
):
    button = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["back_to_home_page"],
                callback_data=f"back_to_{'admin' if is_admin else 'user'}_home_page",
            )
        ],
    ]
    return button


def build_back_button(data: str, lang: str = models.Language.ARABIC.name):
    return [
        InlineKeyboardButton(
            text=BUTTONS[lang]["back_button"],
            callback_data=data,
        ),
    ]


def build_confirmation_keyboard(data: str, lang: str):
    return [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["yes_confirm"],
                callback_data=f"yes_{data}",
            ),
            InlineKeyboardButton(
                text=BUTTONS[lang]["no_confirm"],
                callback_data=f"no_{data}",
            ),
        ]
    ]


def build_request_buttons():
    keyboard = [
        [
            KeyboardButton(
                text="معرفة id مستخدم 🆔",
                request_users=KeyboardButtonRequestUsers(
                    request_id=0, user_is_bot=False
                ),
            ),
            KeyboardButton(
                text="معرفة id قناة 📢",
                request_chat=KeyboardButtonRequestChat(
                    request_id=1, chat_is_channel=True
                ),
            ),
        ],
        [
            KeyboardButton(
                text="معرفة id مجموعة 👥",
                request_chat=KeyboardButtonRequestChat(
                    request_id=2, chat_is_channel=False
                ),
            ),
            KeyboardButton(
                text="معرفة id بوت 🤖",
                request_users=KeyboardButtonRequestUsers(
                    request_id=3, user_is_bot=True
                ),
            ),
        ],
    ]
    return keyboard


def build_keyboard(columns: int, texts: list, buttons_data: list):
    if len(texts) != len(buttons_data):
        raise ValueError("The length of 'texts' and 'buttons_data' must be the same.")

    keyboard = []
    for i in range(0, len(buttons_data), columns):
        row = [
            InlineKeyboardButton(
                text=texts[i + j],
                callback_data=buttons_data[i + j],
            )
            for j in range(columns)
            if i + j < len(buttons_data)
        ]
        if row:  # Only append non-empty rows
            keyboard.append(row)
    return keyboard


def build_payemnt_methods_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                text=method.value,
                callback_data=method.name,
            )
        ]
        for method in models.PaymentMethodName
    ]
    return keyboard


def build_handle_charge_order_keyboard(order_id: int):
    keyboard = [
        [
            InlineKeyboardButton(
                text="تأكيد ✅",
                callback_data=f"approve_charge_order_{order_id}",
            ),
            InlineKeyboardButton(
                text="إلغاء ❌",
                callback_data=f"decline_charge_order_{order_id}",
            ),
        ]
    ]
    return keyboard
