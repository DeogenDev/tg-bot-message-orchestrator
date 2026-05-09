"""Хендлер для работы с сообщениями."""

import logging

from typing import Optional
from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.fsm.context import FSMContext

from src.bot.utils.texts import Texts
from src.bot.utils.buttons import Buttons
from src.bot.utils.states import InputStates

from src.core.interfaces.channels_service import ChannelServiceBase
from src.core.interfaces.messages_service import MessagesServiceBase
from src.core.schemas.message import MessageModel, DeleteMessageModel, ButtonModel


logger = logging.getLogger(__name__)
router = Router()



def build_keyboard_from_models(buttons: list[ButtonModel]) -> Optional[InlineKeyboardMarkup]:

    if not buttons:
        return None

    builder = InlineKeyboardBuilder()
    
    # Сортируем кнопки по рядам, чтобы они шли по порядку
    sorted_buttons = sorted(buttons, key=lambda b: (b.row, b.column))
    
    # Группируем кнопки по рядам
    rows: dict[int, list[ButtonModel]] = {}
    for btn in sorted_buttons:
        rows.setdefault(btn.row, []).append(btn)
    
    # Добавляем кнопки в билдер построчно
    for row_index in sorted(rows.keys()):
        row_btns = [
            InlineKeyboardButton(text=btn.text, url=btn.url) 
            for btn in rows[row_index]
        ]
        builder.row(*row_btns)
    
    return builder.as_markup()


@router.callback_query(F.data == "add_message")
async def add_message_handler(
    callback_query: CallbackQuery,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons
) -> None:
    await callback_query.message.edit_text(
        texts.messages.INPUT_MESSAGE_TEXT,
        reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
    )

    await state.set_state(InputStates.message_text)


@router.message(InputStates.message_text)
async def add_message_handler_text(
    message: Message,
    state: FSMContext,
    messages_service: MessagesServiceBase,
    texts: Texts,
    buttons: Buttons
) -> None:

    await state.clear()

    message_model = MessageModel(
        text=message.text,
    )

    text = texts.messages.FAIL_ADD_MESSAGE

    try:
        await messages_service.add_message(message_model)
        text = texts.messages.SUCCESS_ADD_MESSAGE
    except Exception as e:
        logger.error(f"Ошибка при добавлении сообщения: {e}")

    try:
        await message.answer(
            text=text,
            reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
        )
    except Exception as e:
        logger.warning(f"Не удалось отправить сообщение: {e}")


@router.callback_query(F.data == "delete_message")
async def choice_delete_message_handler(
    callback_query: CallbackQuery,
    texts: Texts,
    buttons: Buttons,
    messages_service: MessagesServiceBase,
) -> None:
    messages = await messages_service.get_messages()

    if not messages:
        await callback_query.message.edit_text(
            texts.messages.NO_MESSAGES,
            reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
        )
        return

    messages_buttons = []

    for message in messages:
        messages_buttons.append(
            InlineKeyboardButton(
                text=message.text,
                callback_data=f"delete_message_id:{message.id}"
            )
        )

    messages_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            messages_buttons,
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="config_messages"
                )
            ]
        ]
    )

    await callback_query.message.edit_text(
        texts.messages.ABOUT_MESSAGES_INFO,
        reply_markup=messages_keyboard
    )


@router.callback_query(F.data.startswith("delete_message_id:"))
async def delete_message_handler_callback(
    callback_query: CallbackQuery,
    texts: Texts,
    buttons: Buttons,
    messages_service: MessagesServiceBase,
) -> None:
    message_id = callback_query.data.split(":")[1]

    delete_message_model = DeleteMessageModel(
        id=int(message_id)
    )
    text = texts.messages.FAIL_DELETE_MESSAGE

    try:
        await messages_service.delete_message(delete_message_model)
        text = texts.messages.DELETE_MESSAGE
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения: {e}")

    try:
        await callback_query.message.edit_text(
            text=text,
            reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
        )
    except Exception as e:
        logger.warning(f"Не удалось обновить сообщение: {e}")


@router.callback_query(F.data == "open_messages")
async def open_message_handler(
    callback_query: CallbackQuery,
    texts: Texts,
    buttons: Buttons,
    messages_service: MessagesServiceBase
) -> None:
    messages = await messages_service.get_messages()

    if not messages:
        await callback_query.message.edit_text(
            texts.messages.NO_MESSAGES,
            reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
        )
        return

    messages_buttons = []

    for message in messages:
        if len(message.text) > 13:  # 5 (начало) + 3 (...) + 5 (конец) = 13
            button_text = f"{message.text[:5]}...{message.text[-5:]}"
        else:
            button_text = message.text
        messages_buttons.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"open_message_id:{message.id}"
            )
        )

    messages_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            messages_buttons,
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="config_messages"
                )
            ]
        ]
    )

    await callback_query.message.edit_text(
        texts.messages.ABOUT_MESSAGES_INFO,
        reply_markup=messages_keyboard
    )


@router.callback_query(F.data.startswith("open_message_id:"))
async def open_message_handler_callback(
    callback_query: CallbackQuery,
    texts: Texts,
    buttons: Buttons,
    state: FSMContext,
    messages_service: MessagesServiceBase
) -> None:
    message_id = callback_query.data.split(":")[1]
    await state.update_data(open_message_id=int(message_id))

    await callback_query.message.edit_text(
        text=texts.messages.OPEN_MESSAGE_INFO,
        reply_markup=buttons.MESSAGES_CONFIG_EDIT_BUTTONS
    )


@router.callback_query(F.data == "send_message_to_channel")
async def send_message_to_channel_handler(
    callback_query: CallbackQuery,
    texts: Texts,
    buttons: Buttons,
    channel_service: ChannelServiceBase
) -> None:
    channels = await channel_service.get_channels()

    if not channels:
        await callback_query.message.edit_text(
            texts.channels.NO_CHANNELS,
            reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
        )
        return

    channels_buttons = []

    for channel in channels:
        channels_buttons.append(
            InlineKeyboardButton(
                text=channel.title,
                callback_data=f"send_message:{channel.channel_id}"
            )
        )

    channels_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            channels_buttons,
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="config_messages"
                )
            ]
        ]
    )

    await callback_query.message.edit_text(
        texts.messages.SEND_MESSAGE_TO_CHANNEL,
        reply_markup=channels_keyboard
    )

@router.callback_query(F.data.startswith("send_message:"))
async def send_message_to_channel_handler_callback(
    callback_query: CallbackQuery,
    texts: Texts,
    buttons: Buttons,
    state: FSMContext,
    message_service: MessagesServiceBase
) -> None:
    channel_id = callback_query.data.split(":")[1]

    state_data = await state.get_data()
    message_id = state_data["open_message_id"]
    text = texts.messages.FAIL_SEND_MESSAGE
    try: 
        message_model = await message_service.get_message(id=message_id)

        message_keyboard = build_keyboard_from_models(message_model.buttons)
        
        await callback_query.bot.send_message(
            chat_id=int(channel_id),
            text=message_model.text,
            reply_markup=message_keyboard
        )

        text = texts.messages.SUCCESS_SEND_MESSAGE
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в канал: {e}")

    await callback_query.message.edit_text(
        text=text,
        reply_markup=buttons.RETURN_TO_MESSAGES_CONFIG_BUTTONS
    )
