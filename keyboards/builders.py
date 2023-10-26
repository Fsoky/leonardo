from typing import Union, Optional, List, Any
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def reply_builder(
    text: Union[str, List[str]],
    sizes: Union[int, List[int]]=2,
    **kwargs
) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    if isinstance(sizes, int):
        sizes = [sizes]

    [
        builder.button(text=txt)
        for txt in text
    ]

    builder.adjust(*sizes)
    return builder.as_markup(resize_keyboard=True, **kwargs)


def inline_builder(
    text: Union[str, List[str]],
    callback_data: Union[Optional[str], Optional[List[str]], None]=None,
    sizes: Union[int, List[int]]=2,
    **kwargs
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    if isinstance(callback_data, str):
        callback_data = [callback_data]
    if isinstance(sizes, int):
        sizes = [sizes]

    [
        builder.button(text=txt, callback_data=cb)
        for txt, cb in zip(text, callback_data)
    ]

    builder.adjust(*sizes)
    return builder.as_markup(**kwargs)
