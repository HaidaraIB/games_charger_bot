from telegram import InlineKeyboardButton
import models
from common.common import format_float
from common.lang_dicts import *


def build_my_orders_keyboard(lang: str):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["charge_orders"],
                callback_data="my_charge_orders",
            ),
            InlineKeyboardButton(
                text=BUTTONS[lang]["buy_orders"],
                callback_data="my_buy_orders",
            ),
        ],
    ]
    return keyboard


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


def stringify_charge_order(
    charge_order: models.ChargeOrder,
    for_admin=True,
    lang: str = models.Language.ARABIC.name,
):
    if for_admin:
        user = models.User.get_by(conds={"user_id": charge_order.user_id})
        return (
            "طلب شحن رصيد 💳\n\n"
            f"آيدي المستخدم: <code>{user.user_id}</code>\n"
            f"اسمه: {f'@{user.username}' if user.username else f'<b>{user.name}</b>'}\n"
            f"اللغة: <i><b>{user.lang.value}</b></i>\n"
            f"رصيده الحالي: <b>{format_float(user.balance)}$</b>\n"
            f"وسيلة الدفع: <b>{charge_order.payment_method_name.value}</b>\n"
            f"المبلغ: <b>{format_float(charge_order.amount)}$</b>\n"
            f"حالة الطلب: <b>{charge_order.status.value[lang]}</b>\n"
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
    else:
        if lang == models.Language.ARABIC.name:
            return (
                "تفاصيل طلب شحن رصيد 💳\n\n"
                f"وسيلة الدفع: <b>{charge_order.payment_method_name.value}</b>\n"
                f"المبلغ: <b>{format_float(charge_order.amount)}$</b>\n"
                f"حالة الطلب: <b>{charge_order.status.value[lang]}</b>\n"
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
        else:
            return (
                "Buy Order Details 💳\n\n"
                f"Payment Method: <b>{charge_order.payment_method_name.value}</b>\n"
                f"Amount: <b>{format_float(charge_order.amount)}$</b>\n"
                f"Order Status: <b>{charge_order.status.value[lang]}</b>\n"
                + (
                    f"Operation Number: <code>{charge_order.operation_number}</code>\n"
                    if charge_order.operation_number
                    else ""
                )
                + f"Order Date:\n<b>{charge_order.order_date.strftime('%Y-%m-%d %H:%M:%S')}</b>\n"
                + (
                    f"Approve Date:\n<b>{charge_order.approve_date.strftime('%Y-%m-%d %H:%M:%S')}</b>\n"
                    if charge_order.approve_date
                    else ""
                )
                + (
                    (
                        f"Decline Date:\n<b>{charge_order.decline_date.strftime('%Y-%m-%d %H:%M:%S')}</b>\n"
                        f"Decline Reason:\n<b>{charge_order.decline_reason}</b>"
                    )
                    if charge_order.decline_date
                    else ""
                )
            )


def stringify_buy_order(
    buy_order: models.BuyOrder,
    order_status: str,
    lang: str,
):
    if lang == models.Language.ARABIC.name:
        return (
            "تفاصيل طلب شراء 🛒\n\n"
            f"رقم الطلب: <code>{buy_order.order_id}</code>\n"
            f"حالة الطلب: <i><b>{order_status}</b></i>\n"
            f"المنتج: <b>{BUTTONS[lang][buy_order.product]}</b>\n"
            f"المجموعة: <b>{BUTTONS[lang][buy_order.group]}</b>\n"
            f"الباقة: <b>{buy_order.category}</b>\n"
            f"السعر: <b>{format_float(buy_order.price)}$</b>\n"
            f"رقم الحساب: <code>{buy_order.urlsocial}</code>\n"
            f"تاريخ الطلب:\n<b>{buy_order.order_date.strftime('%Y-%m-%d %H:%M:%S')}</b>"
        )
    elif lang == models.Language.ENGLISH.name:
        return (
            "Buy Order Details 🛒\n\n"
            f"Order ID: <code>{buy_order.order_id}</code>\n"
            f"Order Status: <i><b>{order_status}</b></i>\n"
            f"Product: <b>{BUTTONS[lang][buy_order.product]}</b>\n"
            f"Group: <b>{BUTTONS[lang][buy_order.group]}</b>\n"
            f"Category: <b>{buy_order.category}</b>\n"
            f"Price: <b>{format_float(buy_order.price)}$</b>\n"
            f"Player ID: <code>{buy_order.urlsocial}</code>\n"
            f"Order Date:\n<b>{buy_order.order_date.strftime('%Y-%m-%d %H:%M:%S')}</b>"
        )
