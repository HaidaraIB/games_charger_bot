from telegram import Update
from telegram.ext import CallbackQueryHandler, InvalidCallbackData
from start import start_command, admin_command
from common.common import invalid_callback_data, create_folders
from common.back_to_home_page import (
    back_to_admin_home_page_handler,
    back_to_user_home_page_handler,
)
from common.error_handler import error_handler
from common.force_join import check_joined_handler

from user.user_calls import *
from user.user_settings import *
from user.products import *
from user.account_settings import *

from admin.admin_calls import *
from admin.admin_settings import *
from admin.broadcast import *
from admin.ban import *
from admin.payment_methods_settings import *
from admin.handle_charge_orders import *

from models import create_tables

from MyApp import MyApp


def main():
    create_folders()
    create_tables()

    app = MyApp.build_app()

    app.add_handler(
        CallbackQueryHandler(
            callback=invalid_callback_data, pattern=InvalidCallbackData
        )
    )

    app.add_handler(user_settings_handler)
    app.add_handler(change_lang_handler)

    app.add_handler(products_handler)
    app.add_handler(charge_account_handler)
    app.add_handler(account_info_handler)

    app.add_handler(add_payment_method_address_handler)
    app.add_handler(del_payment_method_address_handler)
    app.add_handler(payment_methods_settings_handler)
    app.add_handler(choose_payemnt_method_handler)

    app.add_handler(handle_charge_orders_handler)
    app.add_handler(back_to_handle_charge_orders_handler)
    app.add_handler(get_charge_order_decline_reason_handler)
    app.add_handler(get_charge_order_amount_handler)

    # ADMIN SETTINGS
    app.add_handler(admin_settings_handler)
    app.add_handler(show_admins_handler)
    app.add_handler(add_admin_handler)
    app.add_handler(remove_admin_handler)

    app.add_handler(broadcast_message_handler)

    app.add_handler(check_joined_handler)

    app.add_handler(ban_unban_user_handler)

    app.add_handler(admin_command)
    app.add_handler(start_command)
    app.add_handler(find_id_handler)
    app.add_handler(hide_ids_keyboard_handler)
    app.add_handler(back_to_user_home_page_handler)
    app.add_handler(back_to_admin_home_page_handler)

    app.add_error_handler(error_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)
