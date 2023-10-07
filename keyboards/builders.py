from aiogram.utils.keyboard import ReplyKeyboardBuilder


def form_btn(text: str | list) -> ReplyKeyboardBuilder:
    if isinstance(text, str):
        text = [text]
    
    builder = ReplyKeyboardBuilder()
    [builder.button(text=txt) for txt in text]
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )