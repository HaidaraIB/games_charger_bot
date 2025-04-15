from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from telegram.constants import ChatType
import uuid
from common.keyboards import build_request_buttons
from common.constants import *
from common.lang_dicts import *
from Config import Config
import logging
import os
from datetime import datetime
import models

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
if Config.OWNER_ID != 755501092:
    logging.getLogger("httpx").setLevel(logging.WARNING)


def check_hidden_keyboard(context: ContextTypes.DEFAULT_TYPE):
    if (
        not context.user_data.get("request_keyboard_hidden", None)
        or not context.user_data["request_keyboard_hidden"]
    ):
        context.user_data["request_keyboard_hidden"] = False
        request_buttons = build_request_buttons()
        reply_markup = ReplyKeyboardMarkup(request_buttons, resize_keyboard=True)
    else:
        reply_markup = ReplyKeyboardRemove()
    return reply_markup


def uuid_generator():
    return uuid.uuid4().hex


def create_folders():
    os.makedirs("data", exist_ok=True)


async def invalid_callback_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.callback_query.answer("انتهت صلاحية هذا الزر")


def get_lang(user_id: int):
    return models.User.get_by(conds={"user_id": user_id}).lang.name


def format_float(f: float):
    return f"{float(f):,.2f}".rstrip("0").rstrip(".")


async def check_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    referred_lang = get_lang(update.effective_user.id)
    if context.args:
        link_code = context.args[0]
        referral_link = models.ReferralLink.get_by(conds={"link_code": link_code})
        if referral_link:
            inviter = models.User.get_by({"user_id": referral_link.user_id})
            await models.ReferralRelation.add(
                vals={
                    "inviter_id": referral_link.user_id,
                    "referred_id": update.effective_user.id,
                    "link_code": link_code,
                    "join_date": datetime.now(TIMEZONE),
                }
            )
            await update.message.reply_text(
                text=TEXTS[referred_lang]["referral_registered"].format(
                    f"@{inviter.username}"
                    if inviter.username
                    else f"<b>{inviter.name}</b>"
                )
            )
            await context.bot.send_message(
                chat_id=inviter.user_id,
                text=TEXTS[inviter.lang.name]["new_referral_notification"].format(link_code),
            )
