from telegram import InlineKeyboardButton
from common.lang_dicts import *
import models
from telegram.helpers import create_deep_linked_url


def build_settings_keyboard(lang: str):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["lang"],
                callback_data="change_lang",
            )
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["referral"],
                callback_data="referral",
            ),
        ],
    ]
    return keyboard


def build_referral_keyboard(lang: str):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["create_new_referral_link"],
                callback_data="create_new_referral_link",
            ),
            InlineKeyboardButton(
                text=BUTTONS[lang]["revoke_referral_link"],
                callback_data="revoke_referral_link",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["referral_stats"],
                callback_data="referral_stats",
            ),
        ],
    ]
    return keyboard


def stringify_referral_stats(user: models.User, bot_username: str, lang: str):
    relations_count_by_link = models.ReferralRelation.count_relations_by_link(
        user_id=user.user_id
    )
    referred_relation = models.ReferralRelation.get_by(
        conds={"referred_id": user.user_id}
    )
    if lang == models.Language.ARABIC.name:
        return (
            "إحصائيات الإحالة 📊\n\n"
            "روابط الإحالة الحالية:"
            + (
                (
                    "\n"
                    + "\n".join(
                        [
                            f"<code>{create_deep_linked_url(bot_username=bot_username, payload=referral_link.link_code)}</code>"
                            for referral_link in user.referral_links
                        ]
                    )
                )
                if user.referral_links
                else " <b>لا يوجد</b>"
            )
            + "\n\n"
            "الإحالات حسب كود الإحالة:"
            + (
                (
                    "\n"
                    + "\n".join(
                        [
                            f"<code>{relation_count[0]}</code>: <b>{relation_count[1]}</b>"
                            for relation_count in relations_count_by_link
                        ]
                    )
                    + f"\nالإجمالي: <b>{sum([int(relation_count[1]) for relation_count in relations_count_by_link])}</b>"
                )
                if relations_count_by_link
                else " <b>لا يوجد</b>"
            )
            + "\n\n"
            + f"رابط الإحالة الذي قمت بالتسجيل منه:"(
                (
                    "\n"
                    f"♦️ <code>{create_deep_linked_url(bot_username=bot_username, payload=referred_relation.link_code)}</code>"
                )
                if referred_relation
                else "<b>لا يوجد</b>"
            )
        )
    else:
        return (
            "Referrals Statistics 📊\n\n"
            "Current Referral Links:"
            + (
                (
                    "\n"
                    + "\n".join(
                        [
                            f"<code>{create_deep_linked_url(bot_username=bot_username, payload=referral_link.link_code)}</code>"
                            for referral_link in user.referral_links
                        ]
                    )
                )
                if user.referral_links
                else " <b>N/A</b>"
            )
            + "\n\n"
            "Referrals by referral code:"
            + (
                (
                    "\n"
                    + "\n".join(
                        [
                            f"<code>{relation_count[0]}</code>: <b>{relation_count[1]}</b>"
                            for relation_count in relations_count_by_link
                        ]
                    )
                    + f"\nTotal: <b>{sum([int(relation_count[1]) for relation_count in relations_count_by_link])}</b>"
                )
                if relations_count_by_link
                else " <b>N/A</b>"
            )
            + "\n\n"
            + "Referral link you registered from:"(
                (
                    "\n"
                    f"♦️ <code>{create_deep_linked_url(bot_username=bot_username, payload=referred_relation.link_code)}</code>"
                )
                if referred_relation
                else "<b>N/A</b>"
            )
        )
