from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from tgbot.services.paginations.inline_pagination import Page

def categories_list(page:Page):
    cat_list = []
    for item in page:
        cat_list.append(InlineKeyboardButton(text=item.name,
                        callback_data=CategoryList(category_id=item.category_id,name=item.name).pack(),
                        ))
    return cat_list

class CategoryList(CallbackData,prefix="category_list"):
    category_id:int
    name:str

def pagination_markup(markup):
    page_markup = []
    for i,page in enumerate(markup):
        page_markup.append(InlineKeyboardButton(text=str(page),callback_data=PaginatorCallback(page_id=i).pack()))

    return page_markup
class PaginatorCallback(CallbackData,prefix="paginator"):
    page_id:int

def prev_and_forw():
    buttons = []
    buttons.append(InlineKeyboardButton(text="⬅️",callback_data=PrevOrNextCallback(direction="prev").pack()))
    buttons.append(InlineKeyboardButton(text="➡️",callback_data=PrevOrNextCallback(direction="forw").pack()))
    return buttons

class PrevOrNextCallback(CallbackData,prefix="paginator"):
    direction:str

def categories(page:Page,markup,category_id:Optional[int]=None,nested:bool=False):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(*categories_list(page))
    if nested:
        keyboard.button(text="Перейти к товарам",switch_inline_query_current_chat=f"category={category_id}")
        keyboard.button(text="Назад",callback_data="back")
    pg_markup = pagination_markup(markup)
    keyboard.add(*pg_markup)
    keyboard.add(*prev_and_forw())
    keyboard.adjust(max(2,len(pg_markup)))
    return keyboard.as_markup()

#поправить верстку