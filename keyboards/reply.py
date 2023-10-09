from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Моя анкета"),
            KeyboardButton(text="Статистика")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

rmk = ReplyKeyboardRemove()