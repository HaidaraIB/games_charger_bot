from telegram import Chat, Update, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
import models
from user.products.common import (
    build_products_keyboard,
    build_groups_keyboard,
    filter_by_group,
    filter_by_id,
)
from common.common import get_lang, format_float
from common.constants import *
from common.lang_dicts import *
from common.back_to_home_page import back_to_user_home_page_handler
from start import start_command
from common.keyboards import (
    build_back_button,
    build_back_to_home_page_button,
    build_keyboard,
    build_confirmation_keyboard,
    build_user_keyboard,
)
import requests

PRODUCT, GROUP, CATEGORY, URLSOCIAL, CONFIRM_BUY = range(5)


async def products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)
        keyboard = build_products_keyboard(lang)
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=False)[0])
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["choose_product"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return PRODUCT


async def choose_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)
        if not update.callback_query.data.startswith("back"):
            product = update.callback_query.data
            context.user_data["product"] = product
        else:
            product = context.user_data["product"]
        keyboard = build_groups_keyboard(product=product, lang=lang)
        keyboard.append(build_back_button(data="back_to_choose_product", lang=lang))
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=False)[0])

        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["choose_group"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return GROUP


back_to_choose_product = products


async def choose_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)

        if not update.callback_query.data.startswith("back"):
            group = update.callback_query.data
            context.user_data["group"] = group
        else:
            group = context.user_data["group"]

        products = requests.get(
            url=f"{BASE_URL}/products",
            headers=HEADERS,
        )
        categories = filter_by_group(products=products.json(), group=group)

        keyboard = build_keyboard(
            columns=1,
            texts=[category["name"] for category in categories],
            buttons_data=[str(category["id"]) for category in categories],
        )
        keyboard.append(build_back_button(data="back_to_choose_group", lang=lang))
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=False)[0])

        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["choose_category"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return CATEGORY


back_to_choose_group = choose_product


async def choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)

        if not update.callback_query.data.startswith("back"):
            category_id = int(update.callback_query.data)
            context.user_data["category_id"] = category_id
        else:
            category_id = context.user_data["category_id"]

        products = requests.get(
            url=f"{BASE_URL}/products",
            headers=HEADERS,
        )
        category = filter_by_id(products=products.json(), category_id=category_id)
        if category["stock_status"] == "outofstock":
            await update.callback_query.answer(
                text=TEXTS[lang]["category_out_of_stock"],
                show_alert=True,
            )
            return

        context.user_data["final_price"] = category["final_price"] + (
            category["final_price"] * 0.1
        )

        user = models.User.get_by(conds={"user_id": update.effective_user.id})
        if category["final_price"] > user.balance:
            await update.callback_query.answer(
                text=TEXTS[lang]["not_enough_balance"].format(
                    format_float(context.user_data["final_price"]),
                    format_float(user.balance),
                ),
                show_alert=True,
            )
            return

        back_buttons = [
            build_back_button(data="back_to_choose_category", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=False)[0],
        ]

        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["send_urlsocial"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return URLSOCIAL


back_to_choose_category = choose_group


async def get_urlsocial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)
        if update.message:
            urlsocial = update.message.text
            context.user_data["urlsocial"] = urlsocial
        else:
            urlsocial = context.user_data["urlsocial"]

        products = requests.get(
            url=f"{BASE_URL}/products",
            headers=HEADERS,
        )
        category_id = context.user_data["category_id"]
        category = filter_by_id(products=products.json(), category_id=category_id)
        user = models.User.get_by(conds={"user_id": update.effective_user.id})

        keyboard = build_confirmation_keyboard(data="buy_category", lang=lang)
        keyboard.append(build_back_button(data="back_to_get_urlsocial", lang=lang))
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=False)[0])

        if update.message:
            await update.message.reply_text(
                text=TEXTS[lang]["confirm_buy"].format(
                    category["name"],
                    format_float(context.user_data["final_price"]),
                    format_float(user.balance),
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["confirm_buy"].format(
                    category["name"],
                    format_float(context.user_data["final_price"]),
                    format_float(user.balance),
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return CONFIRM_BUY


back_to_get_urlsocial = choose_category


async def confirm_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)

        if update.callback_query.data.startswith("no"):
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["home_page"],
                reply_markup=build_user_keyboard(lang=lang),
            )
            return ConversationHandler.END

        user = models.User.get_by(conds={"user_id": update.effective_user.id})
        await user.update_one(
            update_dict={
                "balance": user.balance - context.user_data["final_price"],
            }
        )

        create_order = requests.post(
            url=f"{BASE_URL}/create-order",
            headers=HEADERS,
            json={
                "product_id": context.user_data["category_id"],
                "quantity": 1,
                "urlsocial": context.user_data["urlsocial"],
            },
        )
        order_info = create_order.json()

        if order_info["success"]:
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["create_order_success"].format(order_info["order_id"]),
                reply_markup=build_user_keyboard(),
            )
        else:
            await user.update_one(update_dict={"balance": user.balance})
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["create_order_fail"],
                reply_markup=build_user_keyboard(),
            )
        return ConversationHandler.END


products_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            products,
            "^products$",
        ),
    ],
    states={
        PRODUCT: [
            CallbackQueryHandler(
                choose_product,
                "^((pubg)|(freefire)|(jawaker))$",
            ),
        ],
        GROUP: [
            CallbackQueryHandler(
                choose_group,
                "^((tokens)|(memberships)|(diamonds)|(uc_bundles))$",
            ),
        ],
        CATEGORY: [
            CallbackQueryHandler(
                choose_category,
                "^[0-9]+$",
            ),
        ],
        URLSOCIAL: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=get_urlsocial,
            ),
        ],
        CONFIRM_BUY: [
            CallbackQueryHandler(confirm_buy, "^((yes)|(no))_buy_category"),
        ],
    },
    fallbacks=[
        start_command,
        back_to_user_home_page_handler,
        CallbackQueryHandler(back_to_get_urlsocial, "^back_to_get_urlsocial$"),
        CallbackQueryHandler(back_to_choose_category, "^back_to_choose_category$"),
        CallbackQueryHandler(back_to_choose_group, "^back_to_choose_group$"),
        CallbackQueryHandler(back_to_choose_product, "^back_to_choose_product$"),
    ],
    name="products_conversation",
    persistent=True,
)
