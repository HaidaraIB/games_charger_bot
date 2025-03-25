import models
from common.common import format_float


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
