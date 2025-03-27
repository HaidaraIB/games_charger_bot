from telegram import Chat, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
import models
from user.account_settings.common import stringify_charge_order
from user.account_settings.account_info import account_info_handler
from common.common import get_lang
from common.back_to_home_page import back_to_user_home_page_handler
from common.constants import *
from common.lang_dicts import *
from common.keyboards import (
    build_back_to_home_page_button,
    build_back_button,
    build_user_keyboard,
)
from user.account_settings.common import (
    build_payemnt_methods_keyboard,
    build_handle_charge_order_keyboard,
)
from Config import Config
from datetime import datetime
from start import start_command

PAYMENT_METHOD, SCREENSHOT = range(2)


async def charge_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)
        keyboard = build_payemnt_methods_keyboard()
        keyboard.append(build_back_button(data="back_to_charge_account", lang=lang))
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=False)[0])
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["choose_payment_method"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return PAYMENT_METHOD


async def choose_payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)
        if not update.callback_query.data.startswith("back"):
            payment_method_name = update.callback_query.data
            payment_method = models.PaymentMethod.get_by({"name": payment_method_name})
            if not payment_method.is_on:
                await update.callback_query.answer(
                    text="هذه الوسيلة متوقفة حالياً ❗️",
                    show_alert=True,
                )
                return

            context.user_data["payment_method_name"] = payment_method_name
        else:
            payment_method_name = context.user_data["payment_method_name"]
            payment_method = models.PaymentMethod.get_by({"name": payment_method_name})

        addresses = models.PaymentMethodAddress.get_by(
            conds={"payment_method_name": payment_method_name}, all=True
        )
        back_buttons = [
            build_back_button(data="back_to_choose_payemnt_method", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=False)[0],
        ]
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["send_screenshot"].format(
                "\n".join([f"<code>{address.address}</code>" for address in addresses])
            ),
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return SCREENSHOT


back_to_choose_payemnt_method = charge_account


async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)

        if update.message.photo:
            photo_msg = await context.bot.send_photo(
                chat_id=Config.PHOTOS_ARCHIVE, photo=update.message.photo[-1]
            )
            charge_order_id = await models.ChargeOrder.add(
                vals={
                    "user_id": update.effective_user.id,
                    "payment_method_name": context.user_data["payment_method_name"],
                    "photo": photo_msg.photo[-1].file_id,
                    "order_date": datetime.now(tz=TIMEZONE),
                }
            )
            charge_order = models.ChargeOrder.get_by(conds={"id": charge_order_id})
            await context.bot.send_photo(
                chat_id=Config.OWNER_ID,
                photo=update.message.photo[-1],
                caption=stringify_charge_order(charge_order=charge_order),
                reply_markup=InlineKeyboardMarkup(
                    build_handle_charge_order_keyboard(order_id=charge_order_id)
                ),
            )
        else:
            charge_order_id = await models.ChargeOrder.add(
                vals={
                    "user_id": update.effective_user.id,
                    "payment_method_name": context.user_data["payment_method_name"],
                    "operation_number": update.message.text,
                    "order_date": datetime.now(tz=TIMEZONE),
                }
            )
            charge_order = models.ChargeOrder.get_by(conds={"id": charge_order_id})
            await context.bot.send_message(
                chat_id=Config.OWNER_ID,
                text=stringify_charge_order(charge_order=charge_order),
                reply_markup=InlineKeyboardMarkup(
                    build_handle_charge_order_keyboard(order_id=charge_order_id)
                ),
            )

        await update.message.reply_text(
            text=TEXTS[lang]["charge_order_submited"].format(charge_order.id),
            reply_markup=build_user_keyboard(lang=lang),
        )

        return ConversationHandler.END


charge_account_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            charge_account,
            "^charge_account$",
        ),
    ],
    states={
        PAYMENT_METHOD: [
            CallbackQueryHandler(
                choose_payment_method,
                lambda x: x in [method.name for method in models.PaymentMethodName],
            )
        ],
        SCREENSHOT: [
            MessageHandler(
                filters=filters.Regex("^[0-9]+$") | filters.PHOTO,
                callback=get_screenshot,
            )
        ],
    },
    fallbacks=[
        back_to_user_home_page_handler,
        start_command,
        account_info_handler,
        CallbackQueryHandler(
            back_to_choose_payemnt_method, "^back_to_choose_payemnt_method$"
        ),
    ],
    name="charge_account_conversation",
    persistent=True,
)
