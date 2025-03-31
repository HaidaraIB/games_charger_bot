from telegram import (
    Chat,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonRequestUsers,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from custom_filters import Admin
import models
from common.keyboards import (
    build_back_button,
    build_back_to_home_page_button,
    build_keyboard,
)
from common.lang_dicts import *
from admin.users.common import stringify_user
from start import admin_command
from common.back_to_home_page import back_to_admin_home_page_handler
import requests
from common.constants import *
from user.account_settings.common import stringify_buy_order, stringify_charge_order

USER, USER_ORDERS_TYPE, USER_ORDER = range(3)


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        await update.callback_query.answer()
        await update.callback_query.delete_message()
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=(
                "اختر حساب المستخدم بالضغط على الزر أدناه\n\n"
                "يمكنك إرسال الid برسالة أيضاً\n\n"
                "أو إلغاء العملية بالضغط على /admin."
            ),
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(
                            text="اختيار حساب مستخدم 👤",
                            request_users=KeyboardButtonRequestUsers(
                                request_id=6, user_is_bot=False
                            ),
                        )
                    ]
                ],
                resize_keyboard=True,
            ),
        )
        return USER


async def get_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        if not update.callback_query:
            if update.effective_message.users_shared:
                user_id = update.effective_message.users_shared.users[0].user_id
            elif update.message:
                user_id = int(update.effective_message.text)
            context.user_data["shared_user_id"] = user_id
        else:
            user_id = context.user_data["shared_user_id"]

        user = models.User.get_by(
            conds={
                "user_id": user_id,
            },
        )
        if not user:
            try:
                user_chat = await context.bot.get_chat(chat_id=user_id)
            except:
                await update.message.reply_text(
                    text=(
                        "لم يتم العثور على المستخدم ❌\n"
                        "تأكد من الآيدي أو من أن المستخدم قد بدأ محادثة مع البوت من قبل"
                    ),
                )
                return
            await models.User.add(
                {
                    "user_id": user_chat.id,
                    "username": user_chat.username if user_chat.username else "",
                    "name": user_chat.full_name,
                }
            )
            user = models.User.get_by(
                conds={
                    "user_id": user_id,
                },
            )

        keyboard = [
            [
                InlineKeyboardButton(
                    text=BUTTONS[models.Language.ARABIC.name]["charge_orders"],
                    callback_data="user_charge_orders",
                ),
                InlineKeyboardButton(
                    text=BUTTONS[models.Language.ARABIC.name]["buy_orders"],
                    callback_data="user_buy_orders",
                ),
            ],
            build_back_button("back_to_get_user"),
            build_back_to_home_page_button()[0],
        ]
        if update.message:
            await update.message.reply_text(
                text="تم العثور على المستخدم ✅",
                reply_markup=ReplyKeyboardRemove(),
            )
            await update.message.reply_text(
                text=stringify_user(user),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            await update.callback_query.edit_message_text(
                text=stringify_user(user),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

        return USER_ORDERS_TYPE


back_to_get_user = users


async def choose_user_orders_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        lang = models.Language.ARABIC.name
        if not update.callback_query.data.startswith("back"):
            orders_type = update.callback_query.data
            context.user_data["user_orders_type"] = orders_type
        else:
            orders_type = context.user_data["user_orders_type"]

        user_id = context.user_data["shared_user_id"]
        if orders_type.startswith("user_charge_orders"):
            text = TEXTS[lang]["charge_orders"]
            orders = models.ChargeOrder.get_by(
                conds={"user_id": user_id},
                all=True,
                limit=20,
            )
            prefix = "user_charge_order_"
            order_id = "id"
            orders_type_name = "شحن رصيد"
        elif orders_type.startswith("user_buy_orders"):
            text = TEXTS[lang]["buy_orders"]
            orders = models.BuyOrder.get_by(
                conds={"user_id": user_id},
                all=True,
                limit=20,
            )
            prefix = "user_buy_order_"
            order_id = "order_id"
            orders_type_name = "شراء"

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

        keyboard.append(build_back_button(data="back_to_choose_user_orders_type"))
        keyboard.append(build_back_to_home_page_button()[0])
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return USER_ORDER


back_to_choose_user_orders_type = get_user


async def choose_user_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE and Admin().filter(update):
        lang = models.Language.ARABIC.name
        keyboard = [
            build_back_button(data="back_to_choose_user_order"),
            build_back_to_home_page_button()[0],
        ]

        order_id = int(update.callback_query.data.split("_")[-1])
        if update.callback_query.data.startswith("user_charge_order"):
            charge_order = models.ChargeOrder.get_by(conds={"id": order_id})
            await update.callback_query.edit_message_text(
                text=stringify_charge_order(
                    charge_order=charge_order, for_admin=True, lang=lang
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        elif update.callback_query.data.startswith("user_buy_order"):
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


back_to_choose_user_order = choose_user_orders_type

users_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            users,
            "^users$",
        ),
    ],
    states={
        USER: [
            MessageHandler(
                filters=filters.Regex("^\d+$"),
                callback=get_user,
            ),
            MessageHandler(
                filters=filters.StatusUpdate.USERS_SHARED,
                callback=get_user,
            ),
        ],
        USER_ORDERS_TYPE: [
            CallbackQueryHandler(
                choose_user_orders_type,
                "^user_((charge)|(buy))_orders$",
            )
        ],
        USER_ORDER: [
            CallbackQueryHandler(
                choose_user_order,
                "^user_((charge)|(buy))_order",
            )
        ],
    },
    fallbacks=[
        admin_command,
        back_to_admin_home_page_handler,
        CallbackQueryHandler(back_to_get_user, "^back_to_get_user$"),
        CallbackQueryHandler(
            back_to_choose_user_orders_type, "^back_to_choose_user_orders_type$"
        ),
        CallbackQueryHandler(back_to_choose_user_order, "^back_to_choose_user_order$"),
    ],
)
