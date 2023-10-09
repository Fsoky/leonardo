from aiogram import Router, F
from aiogram.types import Message

from data.database import DataBase
from data.models import Users

router = Router()


@router.message()
async def echo(message: Message, db: DataBase) -> None:
    msg = message.text.lower()

    if msg == "моя анкета":
        data = await db.get(message.from_user.id)
        usr = data.one()
        pattern = {
            "photo": usr.photo,
            "caption": f"{usr.name} {usr.age}, {usr.city}\n{usr.bio}"
        }

        await message.answer_photo(**pattern)