from telegram import Chat, Update, InlineKeyboardMarkup
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
from common.keyboards import (
    build_back_to_home_page_button,
    build_back_button,
    build_admin_keyboard,
)


ADDRESS = range(1)


async def add_payment_method_address(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        back_buttons = [
            build_back_button("back_to_choose_payment_method"),
            build_back_to_home_page_button()[0],
        ]
        await update.callback_query.edit_message_text(
            text="أرسل العنوان الجديد",
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return ADDRESS


async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        address = update.message.text
        await models.PaymentMethodAddress.add(
            vals={
                "payment_method_name": models.PaymentMethodName[
                    context.user_data["payment_method_name"]
                ],
                "address": address,
            }
        )
        await update.message.reply_text(
            text="تمت إضافة العنوان بنجاح ✅",
            reply_markup=build_admin_keyboard(),
        )
        return ConversationHandler.END


add_payment_method_address_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            add_payment_method_address,
            "^add_payment_method_address$",
        ),
    ],
    states={
        ADDRESS: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=get_address,
            ),
        ],
    },
    fallbacks=[
        admin_command,
        choose_payemnt_method_handler,
        back_to_admin_home_page_handler,
    ],
)
