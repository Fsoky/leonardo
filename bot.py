import asyncio
from aiogram import Bot, Dispatcher

import handlers

from data.database import DataBase
from config_reader import config


async def main() -> None:
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()
    db = DataBase("users_db.db", "users")

    await db.create_table()
    dp.include_routers(
        handlers.start.router,
        handlers.questrionaire.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    asyncio.run(main())