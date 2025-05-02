from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    count=State()
    image=State()
    language=State()