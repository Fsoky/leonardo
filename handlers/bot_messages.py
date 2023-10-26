from aiogram import Router, F
from aiogram.types import Message

from data.database import DataBase

router = Router()


@router.message(F.text)
async def echo(message: Message, db: DataBase) -> None:
    msg = message.text.lower()

    if msg == "моя анкета":
        usr = await db.get(message.from_user.id)
        pattern = {
            "photo": usr.photo,
            "caption": f"{usr.name} {usr.age}, {usr.city}\n{usr.bio}"
        }

        await message.answer_photo(**pattern)