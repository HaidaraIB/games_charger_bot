from telegram import (
    Chat,
    Update,
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
from common.keyboards import build_back_button, build_back_to_home_page_button
from admin.users.common import stringify_user
from start import admin_command
from common.back_to_home_page import back_to_admin_home_page_handler

USER = range(1)


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
        if update.effective_message.users_shared:
            user_id = update.effective_message.users_shared.users[0].user_id
        else:
            user_id = int(update.effective_message.text)

        context.user_data["user_id_to_ban_unban"] = user_id

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
            build_back_button("back_to_get_user"),
            build_back_to_home_page_button()[0],
        ]
        await update.message.reply_text(
            text="تم العثور على المستخدم ✅",
            reply_markup=ReplyKeyboardRemove(),
        )
        await update.message.reply_text(
            text=stringify_user(user),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


back_to_get_user = users


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
        ]
    },
    fallbacks=[
        admin_command,
        back_to_admin_home_page_handler,
        CallbackQueryHandler(back_to_get_user, "^back_to_get_user$"),
    ],
)
