from telegram import Chat, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler
import models
from custom_filters import Admin
from admin.payment_methods_settings.common import (
    build_payment_methods_settings_keyboard,
)
from common.keyboards import (
    build_back_to_home_page_button,
    build_back_button,
    build_payemnt_methods_keyboard,
)


async def payment_methods_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        keyboard = build_payemnt_methods_keyboard()
        keyboard.append(build_back_to_home_page_button()[0])
        await update.callback_query.edit_message_text(
            text="اختر وسيلة الدفع 💳",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ConversationHandler.END


async def choose_payemnt_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        if update.callback_query.data.startswith("switch_method_state"):
            payment_method_name = context.user_data["payment_method_name"]
            payment_method = models.PaymentMethod.get_by(
                conds={"name": payment_method_name},
                eager_load=["addresses"],
            )
            await payment_method.update_one(
                update_dict={"is_on": not payment_method.is_on}
            )
            await update.callback_query.answer(
                text=f"تم {'تفعيل' if not payment_method.is_on else 'إلغاء تفعيل'} {payment_method.name.value} بنجاح",
                show_alert=True,
            )

        elif not update.callback_query.data.startswith("back"):
            payment_method_name = update.callback_query.data
            context.user_data["payment_method_name"] = payment_method_name
        else:
            payment_method_name = context.user_data["payment_method_name"]

        payment_method = models.PaymentMethod.get_by(
            conds={"name": payment_method_name},
            eager_load=["addresses"],
        )

        keyboard = build_payment_methods_settings_keyboard(payment_method)
        keyboard.append(build_back_button("back_to_payment_methods_settings"))
        keyboard.append(build_back_to_home_page_button()[0])

        await update.callback_query.edit_message_text(
            text=(
                f"لديك عناوين <b>{payment_method.name.value}</b> التالية:\n"
                + "\n".join(
                    [
                        f"<code>{address.address}</code>"
                        for address in payment_method.addresses
                    ]
                )
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ConversationHandler.END


payment_methods_settings_handler = CallbackQueryHandler(
    payment_methods_settings,
    "^payment_methods_settings$|^back_to_payment_methods_settings$",
)
choose_payemnt_method_handler = CallbackQueryHandler(
    choose_payemnt_method,
    lambda x: x
    in [method.name for method in models.PaymentMethodName]
    + ["back_to_choose_payment_method", "switch_method_state"],
)
