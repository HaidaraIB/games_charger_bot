from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from common.keyboards import (
    build_back_to_home_page_button,
    build_back_button,
    build_payemnt_methods_keyboard,
)
import models


def build_payment_methods_settings_keyboard(payment_method: models.PaymentMethod):
    keyboard = [
        [
            InlineKeyboardButton(
                text="إلغاء تفعيل 🔴" if payment_method.is_on else "تفعيل 🟢",
                callback_data="switch_method_state",
            )
        ],
        [
            InlineKeyboardButton(
                text="إضافة عنوان ➕",
                callback_data="add_payment_method_address",
            ),
            InlineKeyboardButton(
                text="حذف عنوان✖️",
                callback_data="del_payment_method_address",
            ),
        ],
    ]
    return keyboard


async def prompt_payment_method(update: Update):
    keyboard = build_payemnt_methods_keyboard()
    keyboard.append(build_back_button("back_to_payment_methods_settings"))
    keyboard.append(build_back_to_home_page_button()[0])
    await update.callback_query.edit_message_text(
        text="اختر وسيلة الدفع 💳",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
