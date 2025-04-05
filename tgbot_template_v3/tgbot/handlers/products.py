from typing import Optional

from aiogram import types, Router,F
from aiogram.utils.media_group import MediaGroupBuilder

from infrastructure.database.models import Product
from infrastructure.database.repo.base import BaseRepo

from tgbot.keyboards.inline.product_detail import product_detail,ProductDetailCallback

product_router = Router()

@product_router.inline_query(F.query=="products_list")
async def get_product_list(query:types.InlineQuery,products:list[Optional[Product]]):
    res = []

    for product in products:
        file_id = product.feature_media.image_url
        article = types.InlineQueryResultArticle(
            id= str(product.product_id),
            title=product.title,
            input_message_content=types.InputTextMessageContent(
                message_text=f'Название: {product.title} \n Описание: {product.description[:25]} \n Цена: {product.price}$',
                
            ),
            thumbnail_url=file_id,
            thumbnail_height=320,
            thumbnail_width=320,
            description=product.description,
            reply_markup=product_detail(product.product_id)

        )
        res.append(article)
    await query.answer(
        results=res, cache_time=0
    )

@product_router.callback_query(ProductDetailCallback.filter(F.product_id))
async def get_product(callback:types.CallbackQuery,repo:BaseRepo,callback_data:ProductDetailCallback):
    await callback.answer()
    product:Product = await repo.products.get_single(callback_data.product_id)
    album = MediaGroupBuilder(caption=f"Название: {product.title} \nЦена: {product.price}$\n Описание: {product.description}")
    for media in product.medias:
        album.add_photo(media.telegram_media_id)
    await callback.bot.send_media_group(chat_id=callback.from_user.id,media=album.build())
