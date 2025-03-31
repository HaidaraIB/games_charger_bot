from telegram import Update
from telegram.ext import ContextTypes
from common.force_join import check_if_user_member
import functools
import models
from common.common import check_referral


def check_if_user_banned_dec(func):
    @functools.wraps(func)
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        user = models.User.get_by(
            conds={
                "user_id": update.effective_user.id,
            },
        )
        if user.is_banned:
            return
        return await func(update, context, *args, **kwargs)

    return wrapper


def add_new_user_dec(func):
    @functools.wraps(func)
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        old_user = models.User.get_by(
            conds={
                "user_id": update.effective_user.id,
            },
        )
        if not old_user:
            new_user = update.effective_user
            await models.User.add(
                vals={
                    "user_id": new_user.id,
                    "username": new_user.username if new_user.username else "",
                    "name": new_user.full_name,
                },
            )
            await check_referral(update=update, context=context)
        return await func(update, context, *args, **kwargs)

    return wrapper


def check_if_user_member_decorator(func):
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        is_user_member = await check_if_user_member(update=update, context=context)
        if not is_user_member:
            return
        return await func(update, context, *args, **kwargs)

    return wrapper
