from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

def product_detail(id:int):
    keyboard = InlineKeyboardBuilder()
    #добавить кнопки добавить в корзину или вишлист
    keyboard.button(
        text="Детальная информация",
        callback_data=ProductDetailCallback(product_id=id).pack())
    return  keyboard.as_markup()

class ProductDetailCallback(CallbackData, prefix="product_detail"):
    product_id: int
