from telegram import Chat, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler
import models
from user.account_settings.common import stringify_account
from common.lang_dicts import *
from common.keyboards import build_back_to_home_page_button


async def account_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        user_account = models.User.get_by({"user_id": update.effective_user.id})
        lang = user_account.lang.name
        keyboard = [
            InlineKeyboardButton(
                text=BUTTONS[lang]["charge_account"],
                callback_data="charge_account",
            ),
            build_back_to_home_page_button(lang=lang, is_admin=False)[0][0],
        ]
        await update.callback_query.edit_message_text(
            text=stringify_account(account=user_account),
            reply_markup=InlineKeyboardMarkup.from_column(keyboard),
        )
        return ConversationHandler.END


account_info_handler = CallbackQueryHandler(account_info, "^account_info$|^back_to_account_info$")
