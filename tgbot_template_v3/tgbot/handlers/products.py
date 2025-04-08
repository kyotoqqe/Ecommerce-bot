from typing import Optional

from aiogram import types, Router,F
from aiogram.utils.media_group import MediaGroupBuilder

from infrastructure.database.models import Product
from infrastructure.database.repo.base import BaseRepo

from tgbot.keyboards.inline.product_detail import product_detail,ProductDetailCallback
from tgbot.keyboards.inline.product_menu import product_menu

product_router = Router()

@product_router.inline_query(F.query=="products_list")
async def get_product_list(query:types.InlineQuery,products:list[Optional[Product]]):
    res = []
    category = types.InlineQueryResultArticle(
        id="0",
        title="Категории",
        input_message_content=types.InputTextMessageContent(
            message_text="Категории",
        ),
        thumbnail_url="https://rau.ua/wp-content/uploads/2018/11/Nielsen.jpg"
        ) 
    for product in products:
        file_id = product.feature_media.image_url
        article = types.InlineQueryResultArticle(
            id= str(product.product_id),
            title=product.title,
            input_message_content=types.InputTextMessageContent(
                message_text=f'<a href="{file_id}">&#8203;</a>\nНазвание: {product.title} \nОписание: {product.description[:25]} \n Цена: {product.price}$',
            ),
            thumbnail_url=file_id,
            thumbnail_height=320,
            thumbnail_width=320,
            description=product.description,
            reply_markup=product_detail(product.product_id)

        )
        res.append(category)
        res.append(article)
    await query.answer(
        results=res, cache_time=0,
    )

@product_router.callback_query(ProductDetailCallback.filter(F.product_id))
async def get_product(callback:types.CallbackQuery,repo:BaseRepo,callback_data:ProductDetailCallback):
    await callback.answer()
    product_id = callback_data.product_id
    product = await repo.products.get_single(product_id)
    album = MediaGroupBuilder(caption=f"Название: {product.title} \nЦена: {product.price}$\nОписание: {product.description}")
    for media in product.medias:
        album.add_photo(media.telegram_media_id)
    await callback.bot.send_media_group(chat_id=callback.from_user.id,media=album.build())
    await callback.bot.send_message(chat_id=callback.from_user.id,text="📋Меню товара:",reply_markup=product_menu(product_id))