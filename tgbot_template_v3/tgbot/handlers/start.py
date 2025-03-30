from aiogram import Router, types, F
from aiogram.filters import Command,CommandStart,CommandObject
from aiogram.utils.deep_linking import create_start_link

start_router = Router()

@start_router.message(CommandStart(deep_link=True,deep_link_encoded=True))
async def start_with_referal(message:types.Message,command:CommandObject):
    args = command.args
    await message.answer(f"Ты перешел по реферальной ссылке с параметрами: {args}")

@start_router.message(CommandStart())
async def shop_start(message:types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}. Чтобы пользоваться магазином нажми команду /shop")

@start_router.message(Command("create_referal"))
async def create_referal_link(message:types.Message):
    link = await create_start_link(message.bot, payload="bububu",encode=True)
    await message.answer(f'Твоя реферальная ссылка: {link}. Делись ей с друзьями чтобы получать бонусы на счет')

