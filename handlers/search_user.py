from random import shuffle
import ujson

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.builders import reply_builder, inline_builder
from keyboards.factories import UserAnswerData

from data.database import DataBase

router = Router()
checked_users = {}


@router.message(Command(commands=["search", "view"]))
@router.message(F.text.lower() == "начать поиск")
async def view_user(message: Message, db: DataBase) -> None:
    users = await db.get(all_data=True)
    current_user = await db.get(message.from_user.id)

    try:
        eligible_users = [
            user
            for user in users
            if user.user_id != message.from_user.id
            #and user.look_for != current_user.look_for
            #and user.city == current_user.city
            and user.age - 4 < current_user.age
            and user.age + 4 > current_user.age
        ]
        shuffle(eligible_users)
        user = eligible_users.pop()

        await message.answer_photo(
            user.photo,
            f"{user.name}, {user.age}\n\n"
            f"{user.bio}",
            reply_markup=reply_builder(["👍", "💌", "👎"], 3)
        )
    except IndexError:
        await message.answer("Пользователей вашей категории не найдены!")


@router.message(F.text.in_(["👍", "👎"]))
async def view_new_user(message: Message, state: FSMContext, bot: Bot, db: DataBase) -> None:
    users = await db.get(all_data=True)
    current_user = await db.get(message.from_user.id)

    try:
        eligible_users = [
            user
            for user in users
            if user.user_id != message.from_user.id
            #and user.look_for != current_user.look_for
            #and user.city == current_user.city
            and user.age - 4 < current_user.age
            and user.age + 4 > current_user.age
        ]
        shuffle(eligible_users)
        user = eligible_users.pop()

        await message.answer_photo(
            user.photo,
            f"{user.name}, {user.age}\n\n"
            f"{user.bio}",
            reply_markup=reply_builder(["👍", "💌", "👎"], 3)
        )
    except IndexError:
        await message.answer("Пользователей вашей категории не найдены!")

    if message.text == "👍":
        await bot.send_message(
            user.user_id,
            "Вы понравились одному человеку, хотите посмотреть?",
            reply_markup=inline_builder(
                ["Да", "Нет"],
                [
                    UserAnswerData(
                        answer="yes",
                        user_id=message.from_user.id,
                        username=message.from_user.username
                    ).pack(),
                    UserAnswerData(answer="no").pack()
                ]
            )
        )
        
        new_liked_user = ujson.loads(user.users_liked)
        new_liked_user.append(message.from_user.id)
        await db.user_update(user.user_id, users_liked=ujson.dumps(new_liked_user))
    else:
        pass


@router.callback_query(UserAnswerData.filter(F.answer))
async def show_user_answer_form(
    query: CallbackQuery,
    callback_data: UserAnswerData,
    state: FSMContext,
    db: DataBase
) -> None:
    await state.clear()
    print(callback_data.answer)
    if callback_data.answer == "yes":
        user = await db.get(callback_data.user_id)

        await query.message.answer_photo(
            user.photo,
            f"Приятного общения! "
            f"<a href='tg://user?username={callback_data.username}'>{callback_data.username}</a>\n\n"
            f"{user.name}, {user.age}\n\n{user.bio}"
        )
    await query.answer()