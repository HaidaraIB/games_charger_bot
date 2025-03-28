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
        f"اللغة: <i><b>{user.lang.value}</b></i>\n"
        f"رصيده الحالي: <b>{format_float(user.balance)}</b>\n"
        f"وسيلة الدفع: <b>{charge_order.payment_method_name.value}</b>\n"
        f"حالة الطلب: <b>{charge_order.status.name}</b>\n"
        + (
            f"رقم العملية: <code>{charge_order.operation_number}</code>\n"
            if charge_order.operation_number
            else ""
        )
        + f"تاريخ الطلب:\n<b>{charge_order.order_date.strftime('%Y-%m-%d %H:%M:%S')}</b>\n"
        + (
            f"تاريخ القبول:\n<b>{charge_order.approve_date.strftime('%Y-%m-%d %H:%M:%S')}</b>\n"
            if charge_order.approve_date
            else ""
        )
        + (
            (
                f"تاريخ الرفض:\n<b>{charge_order.decline_date.strftime('%Y-%m-%d %H:%M:%S')}</b>\n"
                f"سبب الرفض:\n<b>{charge_order.decline_reason}</b>"
            )
            if charge_order.decline_date
            else ""
        )
    )
