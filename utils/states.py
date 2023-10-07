from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    age = State()
    city = State()
    sex = State()
    look_for = State()
    about = State()
    photo = State()