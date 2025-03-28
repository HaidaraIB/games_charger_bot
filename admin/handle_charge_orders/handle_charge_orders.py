from telegram import Update, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from custom_filters import Admin, ChargeOrderDeclineReason, ChargeOrderAmount
import models
from common.keyboards import build_back_button, build_handle_charge_order_keyboard
from common.lang_dicts import *
from common.common import get_lang


async def handle_charge_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        event_callback = update.callback_query.data
        if event_callback.startswith("approve"):
            text = "أرسل المبلغ"
        else:
            text = "أرسل سبب الرفض"
        await update.callback_query.answer(
            text=text,
            show_alert=True,
        )
        await update.callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup.from_button(
                build_back_button(f"back_from_{event_callback}")[0]
            ),
        )


async def get_decline_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        order_id = int(
            update.message.reply_to_message.reply_markup.inline_keyboard[0][
                0
            ].callback_data.split("_")[-1]
        )
        decline_reason = update.message.text
        order = models.ChargeOrder.get_by(conds={"id": order_id})
        lang = get_lang(order.user_id)
        await models.ChargeOrder.decline(
            order_id=order_id,
            decline_reason=decline_reason,
        )
        approved_text = "تم الرفض ❌"
        await context.bot.send_message(
            chat_id=order.user_id,
            text=TEXTS[lang]["charge_order_declined"].format(order_id, decline_reason),
        )
        await update.message.reply_text(text=approved_text)
        await context.bot.edit_message_reply_markup(
            chat_id=update.effective_chat.id,
            message_id=update.message.reply_to_message.id,
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(
                    text=approved_text,
                    callback_data=approved_text,
                )
            ),
        )


async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        order_id = int(
            update.message.reply_to_message.reply_markup.inline_keyboard[0][
                0
            ].callback_data.split("_")[-1]
        )
        order = models.ChargeOrder.get_by(conds={"id": order_id})
        lang = get_lang(order.user_id)
        await models.ChargeOrder.approve(
            order_id=order_id,
            user_id=order.user_id,
            amount=float(update.message.text),
        )
        approved_text = "تمت الموافقة ✅"
        await context.bot.send_message(
            chat_id=order.user_id,
            text=TEXTS[lang]["charge_order_approved"].format(order_id),
        )
        await update.message.reply_text(text=approved_text)
        await context.bot.edit_message_reply_markup(
            chat_id=update.effective_chat.id,
            message_id=update.message.reply_to_message.id,
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(
                    text=approved_text,
                    callback_data=approved_text,
                )
            ),
        )


async def back_to_handle_charge_orders(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        order_id = update.callback_query.data.split("_")[-1]
        await update.callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                build_handle_charge_order_keyboard(order_id=order_id)
            ),
        )


back_to_handle_charge_orders_handler = CallbackQueryHandler(
    back_to_handle_charge_orders,
    "^back_from_((approve)|(decline))_charge_order",
)
handle_charge_orders_handler = CallbackQueryHandler(
    handle_charge_orders, "^((approve)|(decline))_charge_order"
)
get_charge_order_amount_handler = MessageHandler(
    filters=ChargeOrderAmount() & filters.Regex("[0-9]+"),
    callback=get_amount,
)
get_charge_order_decline_reason_handler = MessageHandler(
    filters=ChargeOrderDeclineReason() & filters.TEXT & ~filters.COMMAND,
    callback=get_decline_reason,
)
