from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_shop_menu():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="Смотреть товары",
        switch_inline_query_current_chat="products_list"
    )

    keyboard.button(
        text="Корзина",
        callback_data="get_cart"
    )

    keyboard.button(
        text="Профиль",
        callback_data="get_profile"
    )

    keyboard.button(
        text="Тех. поддержка",
        callback_data="techsupport"
    )

    keyboard.button(
        text="Список желаний",
        callback_data="get_wishlist"
    )

    keyboard.button(
        text="Реферальная система",
        callback_data="referal_sys"
    )

    keyboard.adjust(2)

    return keyboard.as_markup()