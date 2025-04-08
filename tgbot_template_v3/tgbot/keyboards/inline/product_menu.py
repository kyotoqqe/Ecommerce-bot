from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.keyboards.inline.buttons.add_to_cart import add_to_cart_button

#возможно стоит все коллбеки типа аддтукарт, аддтувишлист и блабла крч где используется единица товара в один вынести

def product_menu(product_id:int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(add_to_cart_button(product_id))
    return keyboard.as_markup()