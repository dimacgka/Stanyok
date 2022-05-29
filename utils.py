from aiogram.dispatcher.filters.state import State, StatesGroup

class Statements(StatesGroup):
    find = State()
    chief = State()
    auditor = State()