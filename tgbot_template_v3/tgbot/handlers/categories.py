from aiogram import types,Router,F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from infrastructure.database.repo.requests import RequestsRepo


from tgbot.keyboards.inline.categories import categories,CategoryList,PaginatorCallback,PrevOrNextCallback
from tgbot.services.paginations.inline_pagination import Paginator
from tgbot.services.navigation import CategoryNavigator

category_router = Router()

@category_router.message(F.text=="Категории")
@category_router.message(Command("categories"))
async def get_categories(message:types.Message,repo:RequestsRepo):
    categors = await repo.categories.categories_list()
    print(categors)
    paginator = Paginator(categors,24)
    page = paginator.page(1)
    paginator_markup = paginator.get_pages_markup()
    await message.answer("Список категорий:",reply_markup=categories(page,markup=paginator_markup))
       

@category_router.callback_query(CategoryList.filter())
async def get_subcategory(callback:types.CallbackQuery,callback_data:CategoryList,
                          state:FSMContext,repo:RequestsRepo):
    await callback.answer()
    navigator = CategoryNavigator(state)
    await navigator.push(callback_data)
    category_id = callback_data.category_id
    categors = await repo.categories.categories_list(category_id)
    print(categors)
    paginator = Paginator(categors,24)
    page = paginator.page(1)
    paginator_markup = paginator.get_pages_markup()
    await callback.message.edit_text(text=f"Вы сейчас в категории: {callback_data.name}",
                                     reply_markup=categories(page,paginator_markup,category_id,True))

@category_router.callback_query(F.data=="back")
async def go_back_categories(callback:types.CallbackQuery,state:FSMContext,repo:RequestsRepo):
    await callback.answer()
    navigator = CategoryNavigator(state)
    await navigator.pop()
    prev_callback = await navigator.peek()
    if prev_callback:
        category_id = prev_callback.category_id
    else:
        category_id = None
    categors = await repo.categories.categories_list(category_id)
    paginator = Paginator(categors,24)
    page = paginator.page(1)
    paginator_markup = paginator.get_pages_markup()
    nested = bool(prev_callback)
    if nested:
        text=f"Вы сейчас в категории: {prev_callback.name}"
    else:
        text = "Список категорий:"
    await callback.message.edit_text(text=text,
                                     reply_markup=categories(page,paginator_markup,category_id,nested))

