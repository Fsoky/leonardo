from aiogram.filters import BaseFilter
from aiogram.types import Message


class UrlInMessageCheck(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        return message.text.casefold() in ["http", "tg", "www"]