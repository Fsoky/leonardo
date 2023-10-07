from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.reply import main
from data.database import DataBase

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Выберите действие:", reply_markup=main)