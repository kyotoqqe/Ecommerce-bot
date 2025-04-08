from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


def add_to_cart_button(product_id:int):
    return InlineKeyboardButton(text="🛒Добавить в корзину",callback_data=AddToCartCallback(product_id=product_id).pack())

class AddToCartCallback(CallbackData,prefix="add_to_cart"):
    product_id: int