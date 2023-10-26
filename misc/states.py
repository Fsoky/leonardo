from aiogram.fsm.state import StatesGroup, State


class AnswerForm(StatesGroup):
    answer = State()