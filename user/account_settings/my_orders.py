from telegram import Update, Chat, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler
import models
from common.lang_dicts import *
from common.common import get_lang
from common.keyboards import (
    build_back_to_home_page_button,
    build_back_button,
    build_keyboard,
)
from user.account_settings.common import (
    build_my_orders_keyboard,
    stringify_buy_order,
    stringify_charge_order,
)
import requests
from common.constants import *
from user.account_settings.account_info import account_info_handler
from start import start_command
from common.back_to_home_page import back_to_user_home_page_handler

ORDERS_TYPE, ORDER = range(2)


async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)

        keyboard = build_my_orders_keyboard(lang)
        keyboard.append(build_back_button(data="back_to_account_info", lang=lang))
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=False)[0])

        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["my_orders"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ORDERS_TYPE


async def choose_order_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)

        if not update.callback_query.data.startswith("back"):
            orders_type = update.callback_query.data
            context.user_data["orders_type"] = orders_type
        else:
            orders_type = context.user_data["orders_type"]

        if orders_type.startswith("my_charge_orders"):
            text = TEXTS[lang]["charge_orders"]
            orders = models.ChargeOrder.get_by(
                conds={"user_id": update.effective_user.id},
                all=True,
                limit=20,
            )
            prefix = "charge_order_"
            order_id = "id"
            if lang == models.Language.ARABIC.name:
                orders_type_name = "شحن رصيد"
            else:
                orders_type_name = "charge"
        elif orders_type.startswith("my_buy_orders"):
            text = TEXTS[lang]["buy_orders"]
            orders = models.BuyOrder.get_by(
                conds={"user_id": update.effective_user.id},
                all=True,
                limit=20,
            )
            prefix = "buy_order_"
            order_id = "order_id"
            if lang == models.Language.ARABIC.name:
                orders_type_name = "شراء"
            else:
                orders_type_name = "buy"

        if not orders:
            await update.callback_query.answer(
                text=TEXTS[lang]["no_orders_yet"].format(orders_type_name),
                show_alert=True,
            )
            return

        keyboard = build_keyboard(
            columns=3,
            texts=[getattr(order, order_id) for order in orders],
            buttons_data=[f"{prefix}{getattr(order, order_id)}" for order in orders],
        )

        keyboard.append(build_back_button(data="back_to_choose_order_type", lang=lang))
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=False)[0])
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ORDER


back_to_choose_order_type = my_orders


async def choose_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)

        keyboard = [
            build_back_button(data="back_to_choose_order", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=False)[0],
        ]

        order_id = int(update.callback_query.data.split("_")[-1])
        if update.callback_query.data.startswith("charge_order"):
            charge_order = models.ChargeOrder.get_by(conds={"id": order_id})
            await update.callback_query.edit_message_text(
                text=stringify_charge_order(
                    charge_order=charge_order, for_admin=False, lang=lang
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        elif update.callback_query.data.startswith("buy_order"):
            buy_order = requests.post(
                url=f"{BASE_URL}/order",
                headers=HEADERS,
                json={
                    "order_id": order_id,
                },
            )
            buy_order = models.ChargeOrder.get_by(conds={"order_id": order_id})
            await update.callback_query.edit_message_text(
                text=stringify_buy_order(
                    lang=lang, buy_order=buy_order, order_status=buy_order["status"]
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )


back_to_choose_order = choose_order_type

my_orders_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            my_orders,
            "^my_orders$",
        ),
    ],
    states={
        ORDERS_TYPE: [
            CallbackQueryHandler(
                choose_order_type,
                "^my_((charge)|(buy))_orders$",
            ),
        ],
        ORDER: [
            CallbackQueryHandler(
                choose_order,
                "^((charge)|(buy))_order_",
            ),
        ],
    },
    fallbacks=[
        account_info_handler,
        start_command,
        back_to_user_home_page_handler,
        CallbackQueryHandler(back_to_choose_order_type, "^back_to_choose_order_type$"),
        CallbackQueryHandler(back_to_choose_order, "^back_to_choose_order$"),
    ],
    name="my_orders_conversation",
    persistent=True,
)
