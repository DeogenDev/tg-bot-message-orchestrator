"""Кнопки бота."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Настроить сообщения", callback_data="config_messages"),
        ],
        [
            InlineKeyboardButton(text="Настроить каналы", callback_data="config_channels"),
        ]
    ]
)

channels_config = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить канал", callback_data="add_channel"),
            InlineKeyboardButton(text="Удалить канал", callback_data="delete_channel"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="start")
        ]
    ]
)

messages_config = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить сообщение", callback_data="add_message"),
            InlineKeyboardButton(text="Удалить сообщение", callback_data="delete_message"),
        ],
        [
            InlineKeyboardButton(text="Открыть сообщения", callback_data="open_messages"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="start")
        ]
    ]
)

messages_config_edit = InlineKeyboardMarkup(
    inline_keyboard=[
        [   
            InlineKeyboardButton(text="Заменить текст", callback_data="edit_message_text"),
            InlineKeyboardButton(text="Добавить кнопку", callback_data="add_button"),
            InlineKeyboardButton(text="Удалить кнопку", callback_data="delete_button"),
            InlineKeyboardButton(text="Отправить сообщение в канал", callback_data="send_message_to_channel"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="config_messages")
        ]
    ]
)

retutn_to_messages_config = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="config_messages")
        ]
    ]
)

return_to_channels_config = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="config_channels")
        ]
    ]
)


class Buttons:
    START_BUTTONS = start_buttons
    CHANNELS_CONFIG_BUTTONS = channels_config
    MESSAGES_CONFIG_BUTTONS = messages_config
    MESSAGES_CONFIG_EDIT_BUTTONS = messages_config_edit
    RETURN_TO_MESSAGES_CONFIG_BUTTONS = retutn_to_messages_config
    RETURN_TO_CHANNELS_CONFIG_BUTTONS = return_to_channels_config
