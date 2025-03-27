from telegram import InlineKeyboardButton
import models
from common.common import format_float
from datetime import datetime

def stringify_account(account: models.User):
    if account.lang == models.Language.ARABIC:
        return (
            "معلومات الحساب 👤\n\n"
            f"الاسم الكامل 🔤: <i><b>{account.name}</b></i>\n"
            f"الآيدي 🆔: <code>{account.user_id}</code>\n"
            f"الرصيد 💰: <b>{format_float(account.balance)}$</b>"
        )
    elif account.lang == models.Language.ENGLISH:
        return (
            "Account Info 👤\n\n"
            f"Full name 🔤: <i><b>{account.name}</b></i>\n"
            f"User ID 🆔: <code>{account.user_id}</code>\n"
            f"Balance 💰: <b>{format_float(account.balance)}$</b>"
        )


def stringify_charge_order(charge_order: models.ChargeOrder):
    user = models.User.get_by(conds={"user_id": charge_order.user_id})
    return (
        "طلب شحن رصيد 💳\n\n"
        f"آيدي المستخدم: <code>{user.user_id}</code>\n"
        f"اسمه: {f'@{user.username}' if user.username else f'<b>{user.name}</b>'}\n"
        f"رصيده الحالي: <b>{format_float(user.balance)}</b>\n"
        f"وسيلة الدفع: <b>{models.PaymentMethodName(charge_order.payment_method_name).value}</b>\n"
        + (
            f"رقم العملية: <code>{charge_order.operation_number}</code>\n"
            if charge_order.operation_number
            else ""
        )
        + f"تاريخ الطلب:\n<b>{charge_order.order_date.strftime("%Y-%m-%d %H:%M:%S")}</b>"
    )

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


def build_handle_charge_order_keyboard(order_id:int):
    keyboard = [
        [
            InlineKeyboardButton(
                text="تأكيد ✅",
                callback_data=f"verify_order_{order_id}"
            ),
            InlineKeyboardButton(
                text="إلغاء ❌",
                callback_data=f"decline_order_{order_id}"
            ),
        ]
    ]
