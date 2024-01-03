import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation

from tortoise import Tortoise

from handlers import setup_message_routers, QuestionaireScene
from config_reader import config


async def on_startup() -> None:
    await Tortoise.init(
        db_url="sqlite://questionaire.sqlite3",
        modules={"models": ["utils.db_api.models"]}
    )
    await Tortoise.generate_schemas()


async def on_shutdown() -> None:
    await Tortoise.close_connections()


async def main() -> None:
    bot = Bot(config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(events_isolation=SimpleEventIsolation())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    qa_scene = SceneRegistry(dp)
    qa_scene.add(QuestionaireScene)

    message_routers = setup_message_routers()
    dp.include_router(message_routers)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())