from telegram import Chat, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

import models
from custom_filters import Admin
from admin.payment_methods_settings.payment_methods_settings import (
    choose_payemnt_method_handler,
)
from start import admin_command
from common.back_to_home_page import back_to_admin_home_page_handler
from common.keyboards import build_back_to_home_page_button, build_back_button


ADDRESS = range(1)


async def del_payment_method_address(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):

        payment_method_name = context.user_data["payment_method_name"]

        if update.callback_query.data.startswith("del_address"):
            payment_method = models.PaymentMethod.get_by(
                conds={"name": payment_method_name},
                eager_load=["addresses"],
            )
            if len(payment_method.addresses) == 1:
                await update.callback_query.answer(
                    text="كل وسيلة يجب أن تملك عنوان واحد على الأقل ❗️",
                    show_alert=True,
                )
                return

            address_id = int(update.callback_query.data.split("_")[-1])
            await models.PaymentMethodAddress.delete(attr="id", val=address_id)
            await update.callback_query.answer(
                text="تم حذف العنوان بنجاح ✅",
                show_alert=True,
            )

        payment_method = models.PaymentMethod.get_by(
            conds={"name": payment_method_name},
            eager_load=["addresses"],
        )
        keyboard = [
            [
                InlineKeyboardButton(
                    text=address.address,
                    callback_data=f"del_address_{address.id}",
                )
            ]
            for address in payment_method.addresses
        ]
        keyboard.append(build_back_button("back_to_choose_payment_method"))
        keyboard.append(build_back_to_home_page_button()[0])
        await update.callback_query.edit_message_text(
            text="اختر العنوان الذي تريد حذفه",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ADDRESS


del_payment_method_address_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            del_payment_method_address,
            "^del_payment_method_address$",
        ),
    ],
    states={
        ADDRESS: [
            CallbackQueryHandler(del_payment_method_address, "^del_address_"),
        ],
    },
    fallbacks=[
        admin_command,
        choose_payemnt_method_handler,
        back_to_admin_home_page_handler,
    ],
)
