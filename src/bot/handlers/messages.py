"""Хендлер для работы с сообщениями."""

import logging

from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.fsm.context import FSMContext

from src.bot.utils.texts import Texts
from src.bot.utils.buttons import Buttons
from src.bot.utils.states import InputStates


from src.core.interfaces.messages_service import MessagesServiceBase
from src.core.schemas.message import MessageModel, DeleteMessageModel


logger = logging.getLogger(__name__)
router = Router()


@router.message(F == "add_message")
async def add_message_handler(
    message: Message,
    state: FSMContext,
    texts: Texts,
    buttons: Buttons
) -> None:
    await message.answer(
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


@router.callback_query(F == "delete_message")
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


@router.callback_query(F.startwith("delete_message_id:"))
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
