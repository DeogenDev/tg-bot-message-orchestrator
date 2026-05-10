"""Состояния вводов."""

from aiogram.fsm.state import StatesGroup, State


class InputStates(StatesGroup):
    """Состояния вводов."""

    channel_link = State()

    message_text = State()
    edit_message_text = State()

    button_text = State()
    button_url = State()
