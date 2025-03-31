from models.Language import Language

TEXTS = {
    Language.ARABIC.name: {
        "welcome_msg": "أهلاً بك...",
        "force_join_msg": (
            f"لبدء استخدام البوت يجب عليك الانضمام الى قناة البوت أولاً\n\n"
            "اشترك أولاً 👇\n"
            "ثم اضغط <b>تحقق ✅</b>"
        ),
        "join_first_answer": "قم بالاشتراك بالقناة أولاً ❗️",
        "settings": "الإعدادات ⚙️",
        "change_lang": "اختر اللغة 🌐",
        "change_lang_success": "تم تغيير اللغة بنجاح ✅",
        "home_page": "القائمة الرئيسية 🔝",
        "choose_product": "اختر المنتج",
        "choose_group": "اختر المجموعة",
        "choose_category": "اختر الباقة",
        "category_out_of_stock": "هذه الباقة غير متوفرة حالياً ❗️",
        "not_enough_balance": (
            "ليس لديك رصيد كافٍ ❗️\n\n" "سعر الباقة: {}$\n" "رصيدك الحالي: {}$"
        ),
        "send_urlsocial": "أرسل رقم معرف اللاعب أو الID الخاص بك",
        "confirm_buy": (
            "{}\n\n"
            "رقم معرف اللاعب: <code>{}</code>\n"
            "سعر الباقة: <b>{}$</b>\n"
            "رصيدك الحالي: <b>{}$</b>\n\n"
            "هل أنت متأكد من أنك تريد الحصول على هذه الباقة؟"
        ),
        "create_order_success": (
            "تم إنشاء الطلب بنجاح ✅\n\n" "رقم الطلب: <code>{}</code>"
        ),
        "create_order_fail": "حصل خطأ أثناء إنشاء الطلب يرجى إعادة المحاولة لاحقاً ❗️",
        "choose_payment_method": "اختر وسيلة الدفع",
        "send_screenshot": (
            "أرسل المبلغ إلى أحد العناوين التالية:\n"
            "{}\n\n"
            "ثم أرسل لقطة شاشة أو رقم عملية الدفع إلى البوت لنقوم بتوثيقها"
        ),
        "charge_order_submited": (
            "تم إرسال الطلب للمراجعة ✅\n" "رقم الطلب: <code>{}</code>"
        ),
        "charge_order_declined": (
            "للأسف تم رفض طلب شحن الرصيد رقم <code>{}</code> ❌\n" "السبب:\n" "{}"
        ),
        "charge_order_approved": "مبروك تمت الموافقة على طلب شحن الرصيد رقم <code>{}</code> 🎉",
        "my_orders": "طلباتي 📦",
        "charge_orders": (
            "طلبات الشحن 🔌\n\n"
            f"<i>ملاحظة:</i> يتيح البوت العودة إلى آخر 20 طلباً فقط."
        ),
        "buy_orders": (
            "طلبات الشراء 🛒\n\n"
            f"<i>ملاحظة:</i> يتيح البوت العودة إلى آخر 20 طلباً فقط."
        ),
        "no_orders_yet": "ليس لديك طلبات {} بعد ❗️",
        "referral": "الإحالات 🫂",
        "max_referral_links_exceeded": "وصلت إلى الحد الأقصى من روابط الإحالة: 3 روابط ❗️",
        "create_referral_link_success": (
            "رابط الإحالة الجديد الخاص بك:\n"
            "<code>{}</code>\n\n"
            "اضغط /start للمتابعة"
        ),
        "choose_referral_link_to_revoke": "اختر الرابط الذي تريد حذفه",
        "last_referral_link_revoke_attemp": "يجب أن يكون لديك رابط إحالة واحد على الأقل ❗️",
        "you_have_no_referral_links_yet": (
            "ليس لديك روابط إحالة ❗️\n" "يمكنك إنشاء رابط بالضغط على الزر أدناه"
        ),
        "referral_registered": "تم التسجيل عن طريق رابط إحالة {} بنجاح ✅",
        "new_referral_notification": "تسجيل جديد عبر كود الإحالة 🎉: <code>{}</code>",
        "revoke_referral_link_success": "تم حذف رابط الإحالة بنجاح ✅",

    },
    Language.ENGLISH.name: {
        "welcome_msg": "Welcome...",
        "force_join_msg": (
            f"You have to join the bot's channel in order to be able to use it\n\n"
            "Join First 👇\n"
            "And then press <b>Verify ✅</b>"
        ),
        "join_first_answer": "Join the channel first ❗️",
        "settings": "Settings ⚙️",
        "change_lang": "Choose a language 🌐",
        "change_lang_success": "Language changed ✅",
        "home_page": "Home page 🔝",
        "choose_product": "Choose Product",
        "choose_group": "Choose Group",
        "choose_category": "Choose Category",
        "category_out_of_stock": "This category isn't available at the moment ❗️",
        "not_enough_balance": (
            "You don't have enough balance ❗️\n\n"
            "Category price: {}$\n"
            "Your current balance: {}$"
        ),
        "send_urlsocial": "Send your player ID",
        "confirm_buy": (
            "{}\n\n"
            "Player ID: <code>{}</code>\n"
            "Category price: <b>{}$</b>\n"
            "Your current balance: <b>{}$</b>\n\n"
            "Are you sure you want to buy this category?"
        ),
        "create_order_success": (
            "Order created successfully ✅\n\n" "Order ID: <code>{}</code>"
        ),
        "create_order_fail": "An Error occured while creating your order, please try again later ❗️",
        "choose_payment_method": "Choose payment method",
        "send_screenshot": (
            "Send the money to one of the following addresses:\n"
            "{}\n\n"
            "and then send a screenshot of the operation details or just the operation number to the bot in order to verify it"
        ),
        "charge_order_submited": (
            "Order submited successfully ✅\n" "Order ID: <code>{}</code>"
        ),
        "charge_order_declined": (
            "Unfortunately, your charge order number <code>{}</code> has been declined ❌\n"
            "Reason:\n"
            "{}"
        ),
        "charge_order_approved": "Congrats, your charge order number <code>{}</code> has been approved 🎉",
        "my_orders": "My Orders 📦",
        "charge_orders": (
            "Charge Orders 🔌\n\n" f"<i>Note:</i> Only the last 20 orders are shown"
        ),
        "buy_orders": (
            "Buy Orders 🛒\n\n" f"<i>Note:</i> Only the last 20 orders are shown"
        ),
        "no_orders_yet": "You don't have {} orders yet ❗️",
        "referral": "Referrals 🫂",
        "max_referral_links_exceeded": "You've reached the maximum number of referral links allowed: 3 Links ❗️",
        "create_referral_link_success": (
            "Here's Your new Referral link:\n"
            "<code>{}</code>\n\n"
            "press /start to continue"
        ),
        "choose_referral_link_to_revoke": "Choose the link you want to revoke",
        "last_referral_link_revoke_attemp": "You must have at least one Referral link ❗️",
        "you_have_no_referral_links_yet": (
            "You don't have any referral link ❗️\n"
            "you can create one from the button below"
        ),
        "referral_registered": "Successfully registered from {} referral link ✅",
        "new_referral_notification": "New referral from link code 🎉: <code>{}</code>",
        "revoke_referral_link_success": "Succesfully revoked ✅",
    },
}

BUTTONS = {
    Language.ARABIC.name: {
        "yes_confirm": "نعم 👍",
        "no_confirm": "لا 👎",
        "check_joined": "تحقق ✅",
        "bot_channel": "قناة البوت 📢",
        "back_button": "الرجوع 🔙",
        "settings": "الإعدادات ⚙️",
        "lang": "اللغة 🌐",
        "back_to_home_page": "العودة إلى القائمة الرئيسية 🔙",
        "products": "المنتجات 🛍",
        "account_info": "معلومات الحساب 👤",
        "freefire": "فري فاير 💣",
        "pubg": "ببجي 🪖",
        "jawaker": "جواكر ♠️",
        "uc_bundles": "شدات 💵",
        "diamonds": "جواهر 💎",
        "memberships": "عضويات 📝",
        "tokens": "توكنز 🪙",
        "charge_account": "شحن الحساب 💳",
        "my_orders": "طلباتي 📦",
        "charge_orders": "طلبات الشحن 🔌",
        "buy_orders": "طلبات الشراء 🛒",
        "referral": "الإحالات 🫂",
        "create_new_referral_link": "إنشاء رابط إحالة جديد ➕",
        "revoke_referral_link": "حذف رابط إحالة ✖️",
        "referral_stats": "إحصائيات 📊",
    },
    Language.ENGLISH.name: {
        "yes_confirm": "Yes 👍",
        "no_confirm": "No 👎",
        "check_joined": "Verify ✅",
        "bot_channel": "Bot's Channel 📢",
        "back_button": "Back 🔙",
        "settings": "Settings ⚙️",
        "lang": "Language 🌐",
        "back_to_home_page": "Back to home page 🔙",
        "products": "Products 🛍",
        "account_info": "Account Info 👤",
        "freefire": "Free Fire 💣",
        "pubg": "PUBG 🪖",
        "jawaker": "Jawaker ♠️",
        "uc_bundles": "UC Bundles 💵",
        "diamonds": "Diamonds 💎",
        "memberships": "Memberships 📝",
        "tokens": "Tokens 🪙",
        "charge_account": "Charge Account 💳",
        "my_orders": "My Orders 📦",
        "charge_orders": "Charge Orders 🔌",
        "buy_orders": "Buy Orders 🛒",
        "referral": "Referrals 🫂",
        "create_new_referral_link": "Create New Referral Link ➕",
        "revoke_referral_link": "Revoke Referral Link ✖️",
        "referral_stats": "Statistics 📊",
    },
}
