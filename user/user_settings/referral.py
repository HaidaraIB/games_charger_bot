from telegram import Chat, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler
from telegram.helpers import create_deep_linked_url
import models
from common.lang_dicts import *
from common.common import get_lang, uuid_generator
from common.keyboards import (
    build_back_button,
    build_back_to_home_page_button,
    build_keyboard,
)
from user.user_settings.common import build_referral_keyboard
from datetime import datetime
from common.constants import *
from user.user_settings.common import stringify_referral_stats
from user.user_settings.user_settings import user_settings_handler
from start import start_command
from common.back_to_home_page import back_to_user_home_page_handler

REFERRAL_OPTION = range(1)


async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)

        keyboard = build_referral_keyboard(lang=lang)

        keyboard.append(build_back_button(data="back_to_user_settings", lang=lang))
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=False)[0])

        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["referral"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return REFERRAL_OPTION


async def choose_referral_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == Chat.PRIVATE:
        lang = get_lang(update.effective_user.id)

        user = models.User.get_by(
            conds={"user_id": update.effective_user.id},
            eager_load=["referral_links"],
        )

        back_buttons = [
            build_back_button(data="back_to_choose_referral_option", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=False)[0],
        ]

        if update.callback_query.data.endswith("revoke"):
            if len(user.referral_links) == 1:
                await update.callback_query.answer(
                    text=TEXTS[lang]["last_referral_link_revoke_attemp"],
                    show_alert=True,
                )
                return
            link_code = update.callback_query.data.split("_")[0]
            await models.ReferralLink.delete(attr="link_code", val=link_code)
            await update.callback_query.answer(
                text=TEXTS[lang]["revoke_referral_link_success"],
                show_alert=True,
            )
            user = models.User.get_by(
                conds={"user_id": update.effective_user.id},
                eager_load=["referral_links"],
            )
            referral_option = context.user_data["referral_option"]
        elif not update.callback_query.data.startswith("back"):
            referral_option = update.callback_query.data
            context.user_data["referral_option"] = referral_option
        else:
            referral_option = context.user_data["referral_option"]

        if referral_option == "create_new_referral_link":
            if len(user.referral_links) == 3:
                await update.callback_query.answer(
                    text=TEXTS[lang]["max_referral_links_exceeded"],
                    show_alert=True,
                )
                return
            link_code = uuid_generator()
            while models.ReferralLink.get_by(conds={"link_code": link_code}):
                link_code = uuid_generator()
            await models.ReferralLink.add(
                vals={
                    "user_id": update.effective_user.id,
                    "link_code": link_code,
                    "creation_date": datetime.now(TIMEZONE),
                }
            )
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["create_referral_link_success"].format(
                    create_deep_linked_url(
                        bot_username=context.bot.username, payload=link_code
                    )
                )
            )
            return ConversationHandler.END
        elif referral_option == "revoke_referral_link":
            if len(user.referral_links)==0:
                await update.callback_query.answer(
                    text=TEXTS[lang]["you_have_no_referral_links_yet"],
                    show_alert=True,
                )
                return

            keyboard = build_keyboard(
                columns=1,
                texts=[link.link_code for link in user.referral_links],
                buttons_data=[
                    f"{link.link_code}_revoke" for link in user.referral_links
                ],
            )
            keyboard.append(back_buttons[0])
            keyboard.append(back_buttons[1])
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["choose_referral_link_to_revoke"],
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        elif referral_option == "referral_stats":
            await update.callback_query.edit_message_text(
                text=stringify_referral_stats(
                    user=user,
                    bot_username=context.bot.username,
                    lang=lang,
                ),
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )


back_to_choose_referral_option = referral
referral_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            referral,
            "^referral$",
        ),
    ],
    states={
        REFERRAL_OPTION: [
            CallbackQueryHandler(
                choose_referral_option,
                "^referral_stats$|^revoke_referral_link$|^create_new_referral_link$",
            ),
            CallbackQueryHandler(
                choose_referral_option,
                ".+revoke$",
            ),
        ],
    },
    fallbacks=[
        back_to_user_home_page_handler,
        start_command,
        user_settings_handler,
        CallbackQueryHandler(
            back_to_choose_referral_option, "^back_to_choose_referral_option$"
        ),
    ],
    name="referral_conversation",
    persistent=True,
)
