"""TODO:
[] Поставить проверку на город
[] Поставить проверку на кол-во символов (name, bio)
"""

from dataclasses import dataclass
from typing import Any

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, ScenesManager, on

from keyboards import rmk, reply_builder
from utils import Users


@dataclass
class QuestionButtons:
    text: str


@dataclass
class Question:
    text: str
    buttons: list[QuestionButtons] | None = None


QUESTIONS = [
    Question(
        text="Как тебя зовут?",
        buttons=[
            QuestionButtons(text="No name")
        ]
    ),
    Question(text="Сколько тебе лет?"),
    Question(text="Из какого ты города?"),
    Question(
        text="Давай определимся с полом",
        buttons=[
            QuestionButtons(text="Я парень"),
            QuestionButtons(text="Я девушка")
        ]
    ),
    Question(
        text="Кого ты предпочитаешь?",
        buttons=[
            QuestionButtons(text="Пареней"),
            QuestionButtons(text="Девушек"),
            QuestionButtons(text="Мне все равно")
        ]
    ),
    Question(text="Опиши себя"),
    Question(text="Отправь свое фото")
]


class QuestionaireScene(Scene, state="start"):

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, step: int | None=0) -> Any:
        user = await Users.filter(user_id=message.from_user.id).first()
        if user:
            await state.update_data(user_exists=True)
            await self.wizard.exit()

        if not step:
            await message.answer("Давай заполним анкету!", reply_markup=rmk)

        try:
            questionaire = QUESTIONS[step]
        except IndexError:
            return await self.wizard.exit()
        
        markup = reply_builder(
            [btn.text for btn in questionaire.buttons]
        ) if questionaire.buttons else rmk

        await state.update_data(step=step)
        return await message.answer(
            text=QUESTIONS[step].text,
            reply_markup=markup
        )
    
    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        answers = data.get("answers", {})

        if data.get("user_exists"):
            return await message.answer("Добро пожаловать!")

        await Users.create(
            user_id=message.from_user.id,
            name=answers[0],
            age=answers[1],
            city=answers[2],
            sex=answers[3],
            look_for=answers[4],
            bio=answers[5],
            photo=answers[6]
        )
        await message.answer("Ваша анкета создана!")

    @on.message(F.text | F.photo)
    async def answer(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        step = data["step"]
        answers = data.get("answers", {})

        if step == 1 and not message.text.isdigit():
            return await message.answer("Отправь корректное число!")
        if step == 3 and message.text.lower() not in ["я парень", "я девушка"]:
            return await message.answer("Выбери корректный вариант!")
        if step == 4 and message.text.lower() not in ["парни", "девушки", "мне все равно"]:
            return await message.answer("Выбери корректный вариант!")

        if step != 6:
            if message.photo:
                return await message.answer("Отправь текст!")
            answers[step] = message.text
        else:
            if not message.photo:
                return await message.answer("Отправь фото!")
            answers[step] = message.photo[-1].file_id

        await state.update_data(answers=answers)
        await self.wizard.retake(step=step + 1)


router = Router()
router.message.register(QuestionaireScene.as_handler(), Command("start"))


@router.message(Command("start"))
async def start(message: Message, scenes: ScenesManager) -> None:
    await scenes.close()