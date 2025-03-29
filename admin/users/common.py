import models
from common.common import format_float


def stringify_user(user: models.User):
    charge_orders = models.ChargeOrder.get_by(conds={"user_id": user.id})
    if not charge_orders:
        charge_orders = []
    buy_orders = models.BuyOrder.get_by(conds={"user_id": user.id})
    if not buy_orders:
        buy_orders = []
    return (
        "معلومات مستخدم 👤\n\n"
        f"الرقم التسلسلي: <code>{user.id}</code>\n"
        f"الآيدي: <code>{user.user_id}</code>\n"
        f"اسم المستخدم: {f'@{user.username}' if user.username else f'<i>لا يوجد</i>'}\n"
        f"الاسم الكامل: <b>{user.name}</b>\n"
        f"اللغة: <i><b>{user.lang.value}</b></i>\n"
        f"الرصيد: <b>{format_float(user.balance)}</b>\n"
        f"عدد الطلبات: <b>{len(buy_orders)}</b>\n"
        f"إجمالي مبالغ الطلبات: <b>{format_float(sum([order.price for order in buy_orders]))}</b>\n"
        f"عدد مرات الشحن: <b>{len(charge_orders)}</b>\n"
        f"إجمالي مبالغ الشحن: <b>{format_float(sum([order.amount for order in charge_orders]))}</b>\n"
    )
