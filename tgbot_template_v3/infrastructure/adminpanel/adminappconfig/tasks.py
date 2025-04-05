import asyncio
import os

from asgiref.sync import sync_to_async

from aiogram import Bot
from aiogram.types import FSInputFile

from .models import Media
from settings.celery import app

async def send_media(token:str,path:str,id:int,channel_id:int):
    bot = Bot(token=token)
    #сделать нормальную проверку
    print(os.getcwd())
    if not os.path.exists(path):
        print(f"Path {path} not exists")
        return
    media = await sync_to_async(Media.objects.get)(media_id=id)
    media_type = media.media_type
    print(media_type)
    file = FSInputFile(path=path)
    if media_type == "photo":
        photo = await bot.send_photo(chat_id=channel_id,photo=file)
        media.telegram_media_id = photo.photo[-1].file_id
    if media_type == "video":
        video = await bot.send_video(chat_id=channel_id,video=file)
        media.telegram_media_id = video.video.file_id
    
    await sync_to_async(media.save)()
    await bot.session.close()

@app.task
def send_media_task(token:str,path:str,id:int,channel_id:int):
    asyncio.run(send_media(token, path, id, channel_id))