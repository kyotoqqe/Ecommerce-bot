import asyncio
from settings.celery import app
from aiogram import Bot
from aiogram.types import FSInputFile

from .models import Media

async def send_media(token:str,path:str,id:int,channel_id:int):
    print("start")
    bot = Bot(token=token)
    media = Media.objects.get(media_id=id)
    media_type = media.media_type
    file = FSInputFile(filename=path)
    if media_type == "photo":
        photo = await bot.send_photo(chat_id=channel_id,photo=file)
        media.telegram_media_id = photo.photo[-1].file_id
    if media_type == "video":
        video = await bot.send_video(chat_id=channel_id,video=file)
        media.telegram_media_id = video.video.file_id
    
    media.save()
    await bot.session.close()

@app.task
def send_media_task(token:str,path:str,id:int,channel_id:int):
    print("Celery таска запускает asyncio loop...")
    asyncio.run(send_media(token, path, id, channel_id))